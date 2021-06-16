from sys import argv
import subprocess
import pathlib
import os

PROJECT_PATH = str(pathlib.Path().absolute())
FILES_TO_REPLACE_PROJECT_NAME = ['myenv.env', 'docker-compose.yml', 'settings.py']


def setup(project_name):
    subprocess.run(['pipenv', 'run', 'django-admin', 'startproject', project_name])
    for dname, dirs, files in os.walk(PROJECT_PATH):
        for i in [f'{dname}/{f}' for f in files if f in FILES_TO_REPLACE_PROJECT_NAME]:
            with open(i) as to_read, open(i, 'w') as to_write:
                to_write.write(to_read.read().replace('myproject', project_name))


if __name__ == '__main__':
    if argv[-1] == __file__:
        raise Exception('You must provide the project name.')
    setup(argv[-1])
