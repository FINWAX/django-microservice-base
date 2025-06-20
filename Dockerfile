FROM python:3.13-slim

# Create the app and virtualenv directories
RUN mkdir /app /venv

# Set the working directory
WORKDIR /app

# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (for psycopg2-binary)
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry
RUN pip install --upgrade pip
RUN pip install poetry

# Copy the requirements first (better caching)
COPY poetry.lock /app/
COPY pyproject.toml /app/

# Configure Poetry to create virtualenv in /venv and install dependencies
RUN poetry config virtualenvs.path /venv && \
    poetry config virtualenvs.in-project false && \
    poetry install --no-root

# Create user and set permissions
RUN useradd -m -r appuser && \
    chown -R appuser:appuser /app /venv

# Switch to non-root user
USER appuser

RUN poetry config virtualenvs.path /venv && \
    poetry config virtualenvs.in-project false

# Expose the application port
EXPOSE 8088

# Start the application using Gunicorn
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:8088", "--workers", "3", "msvc.wsgi:application"]
