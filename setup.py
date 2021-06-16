from sys import argv
import subprocess
import pathlib
import os

PROJECT_PATH = str(pathlib.Path().absolute())


def setup(project_name):
    params = ['pipenv', 'run', 'django-admin', 'startproject', project_name, '.']
    subprocess.run(params)
    replace_project_name_in_files(project_name)


def replace_project_name_in_files(project_name):
    for dname, dirs, files in os.walk(PROJECT_PATH):
        for file in files:
            if file in ['myenv.env', 'docker-compose.yml', 'settings.py']:
                with open(f'{dname}/{file}') as old_file:
                    new_content = old_file.read().replace('myproject', project_name)
                with open(f'{dname}/{file}', 'w') as new_file:
                    new_file.write(new_content)


def replace_default_database_settings(project_name):
    settings_path = f'{PROJECT_PATH}/{project_name}/settings.py'
    default = '''
        {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    '''
    new_conf = '''
        {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB'),
            'USER': os.environ.get('POSTGRES_USER'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
            'HOST': os.environ.get('POSTGRES_HOST'),
            'POST': 5432,
        }
    '''
    with open(settings_path) as default_settings:
        with open(settings_path) as settings:
            settings.write(default_settings.read().replace(default, new_conf))


if __name__ == '__main__':
    if argv[-1] == __file__:
        raise Exception('You must provide the project name.')
    setup(argv[-1])
