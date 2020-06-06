# caddy-django

Reverse proxy for django apps with alpine linux, caddy, pipenv and postgres.

Important tags:

 - [Caddyfile](https://caddyserver.com/docs/caddyfile) v2
 - Django 3.0 [Docs](https://docs.djangoproject.com/en/3.0/)

requirements:

 1. [Pipenv](https://pipenv.pypa.io/en/latest/)
 2. [Docker](https://docs.docker.com/get-docker/)
 3. [Docker Compose](https://docs.docker.com/compose/install/)


Instructions:

    $ git clone git@github.com:DiegoMagg/caddy-django.git .
    $ pipenv install
    $ docker-compose up --build

Then, go to your browser and type:

    https://localhost

**note:** Caddy automagically set https as described [here](https://caddyserver.com/docs/automatic-https), both firefox and google chrome points an invalid certificate on localhost. Just bypass the alert through advanced settings and see django initial page.

## Caddyfile with domain

    yourdomain.com {
      root /path/to/project
      file_server /static
      reverse_proxy web:8000
    }

Change localhost to your domain and set the project root path.
To serve static files set STATIC_ROOT in project settings as described [here](https://docs.djangoproject.com/en/3.0/howto/static-files/#deployment) .
