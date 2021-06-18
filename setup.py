from sys import argv
import subprocess
import pathlib
from yaml import dump
from re import sub


PROJECT_PATH = str(pathlib.Path().absolute())


def setup(project_name):
    params = ['pipenv', 'run', 'django-admin', 'startproject', project_name, '.']
    subprocess.run(params)
    create_docker_compose_yaml(project_name)
    replace_default_database_settings(project_name)
    create_initial_dot_env(project_name)
    create_caddyfile()


def create_docker_compose_yaml(project_name):
    yaml_dict = {
        "version": "3.7",
        "services": {
            "web": {
                "container_name": f"{project_name}-web",
                "build": {"context": ".", "dockerfile": "Dockerfile"},
                "command": (
                    f"pipenv run gunicorn {project_name}.wsgi"
                    " --bind 0.0.0.0:8000"
                ),
                "env_file": ".env",
                "image": "docker.teste",
                "depends_on": ["postgres"],
                "restart": "on-failure",
                "volumes": [".:/app"],
            },
            "caddy": {
                "image": "caddy:2.3.0-alpine",
                "container_name": f"caddy",
                "links": ["web:web"],
                "ports": ["80:80", "443:443"],
                "volumes": ["./Caddyfile:/etc/caddy/Caddyfile"],
            },
            "migrations": {
                "build": {"context": ".", "dockerfile": "Dockerfile"},
                "command": "pipenv run python manage.py migrate",
                "env_file": ".env",
                "image": "docker.teste",
                "depends_on": ["postgres"],
                "restart": "on-failure",
                "volumes": [".:/app"],
            },
            "postgres": {
                "container_name": f"{project_name}-postgres",
                "image": "postgres:13.3-alpine",
                "volumes": ["postgres_data:/var/lib/postgresql/data/"],
                "restart": "on-failure",
                "env_file": ".env",
            },
        },
        "volumes": {"postgres_data": None},
    }
    create_file('docker-compose.yaml', dump(yaml_dict, sort_keys=False))


def replace_default_database_settings(project_name):
    settings_path = f'{project_name}/settings.py'
    path_lib_str = 'from pathlib import Path'
    new_conf = (
        '{\n'
        "        'ENGINE': 'django.db.backends.postgresql',\n"
        "        'NAME': os.environ.get('POSTGRES_DB'),\n"
        "        'USER': os.environ.get('POSTGRES_USER'),\n"
        "        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),\n"
        "        'HOST': os.environ.get('POSTGRES_HOST'),\n"
        "        'POST': 5432,\n"
        '    },'
    )
    with open(settings_path, 'rt') as default_settings:
        default_settings = default_settings.read()
    settings = default_settings.replace(path_lib_str, f'{path_lib_str}\nimport os\n')
    create_file(
        settings_path,
        sub(
            r"({\n\s*\'E\w+.*)\n\s*\S\w+\S*\s.*\n.*",
            new_conf,
            settings,
        )
    )


def create_caddyfile():
    create_file(
        'Caddyfile',
        (
            'localhost {\n'
            f'  root {PROJECT_PATH}\n'
            '  file_server /static\n'
            '  reverse_proxy web:8000\n'
            '}'
        )
    )


def create_initial_dot_env(project_name):
    create_file(
        '.env',
        (
            f'DJANGO_SETTINGS_MODULE={project_name}.settings\n'
            'POSTGRES_DB=postgres\n'
            'POSTGRES_USER=postgres\n'
            'POSTGRES_PASSWORD=postgres\n'
            'POSTGRES_HOST=postgres\n'
            'PYTHONPATH=.'
        )
    )


def create_file(path, content):
    with open(f'{PROJECT_PATH}/{path}', 'w') as file:
        file.write(content)


if __name__ == '__main__':
    if argv[-1] == __file__:
        raise Exception('You must provide the project name.')
    setup(argv[-1])
