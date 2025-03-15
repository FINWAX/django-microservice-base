# Django Microservice Base

## About

This project is base of microservice implements on Django.

## Usage

### Install

Download and prepare project

```commandline
sh /path-to/scripts/install.sh -u1000 -g1000 -r"FINWAX/django-microservice-base" -d"/destination-path" -p"/previous-path-if-needs-import-data"
```

Then do first launch

```commandline
sh /path_to/scripts/first-launch.sh "/path-to/project"
```

Fill and validate env files for dev/test and production.

Then use

```commandline
sh /path_to/scripts/dev-launch.sh "/path-to/project"
```

or

```commandline
sh /path_to/scripts/prod-launch.sh "/path-to/project"
```

### Update

Use update script

```commandline
sh /path_to/scripts/update.sh -u1000 -g1000 -r"FINWAX/django-microservice-base" -d"/current-path" -p"/path-to-move-current-version"
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
