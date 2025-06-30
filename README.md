# Django Microservice Base

## About

This project is base of microservice implements on Django.

## Usage

Get script

```commandline
git clone --no-checkout --depth 1 https://github.com/FINWAX/django-microservice-base.git temp && cd temp && git sparse-checkout init --cone && git sparse-checkout set scripts && git checkout master && cd .. && mv temp/scripts . && (rm -rf temp 2>/dev/null || Remove-Item -Path temp -Recurse -Force 2>$null)
```

Note: run scripts from the corresponding directory!

```commandline
cd /path_to/scripts
```

### Install

Download project

```commandline
sh ./install.sh -u1000 -g1000 -r"FINWAX/django-microservice-base" -d"/destination-path" -p"/previous-path-if-needs-import-data"
```

Prepare config in `env.dev` and `prod.dev`.

Then do first launch

```commandline
sh ./first-launch.sh "/path-to/project"
```

Fill and validate env files for dev/test and production.

Then use

```commandline
sh ./dev-launch.sh "/path-to/project"
```

or

```commandline
sh ./prod-launch.sh "/path-to/project"
```

### Update

Use update script

```commandline
sh ./update.sh -u1000 -g1000 -r"FINWAX/django-microservice-base" -d"/current-path" -p"/path-to-move-current-version"
```

### Control

If it needs - use `docker compose exec dj ...command`.

Run dev server

```commandline
python manage.py runserver 8088

```

Add migrations for defined models

```commandline
python manage.py makemigrations
```

Provide existing migrations

```commandline
python manage.py migrate
```

Rollback all migrations

```commandline
poetry run python manage.py migrate app zero
```

Flush database

```commandline
poetry run python manage.py flush
```

Collect static files

```commandline
poetry run python manage.py collectstatic --noinput
```

Add superuser

```commandline
poetry run python manage.py createsuperuser
```

### View

Check example endpoints:

- `http://127.0.0.1:8088/health/check` - service works normal
- `http://127.0.0.1:8088/health/availability` - service is available
- `http://127.0.0.1:8088/greeting/hello-protected` - auth via Zitadel
- `http://127.0.0.1:8088/greeting/hello-unprotected?name=Nohj` - GET params passed well

## Links

- [Django documentation](https://docs.djangoproject.com/)
- [Project GitHub](https://github.com/FINWAX/django-microservice-base)
- [FINWAX GitHub](https://github.com/FINWAX)
- [Zitadel Auth](https://zitadel.com/)
