from sys import argv
import subprocess
import pathlib
import os

PROJECT_PATH = str(pathlib.Path().absolute())
FILES_TO_REPLACE_PROJECT_NAME = ['myenv.env', 'docker-compose.yml', 'settings.py']


def setup(project_name):
    # subprocess.run(['pipenv', 'run', 'django-admin', 'startproject', project_name])
    for dname, dirs, files in os.walk(PROJECT_PATH):
        for i in [f'{dname}/{f}' for f in files if f in FILES_TO_REPLACE_PROJECT_NAME]:
            with open(i, 'rw') as file:
                content = file.read()
                content.replace('myproject', project_name)
                file.write(content)
    pass


if __name__ == '__main__':
    if argv[-1] == __file__:
        raise Exception('You must provide the project name.')
    setup(argv[-1])
