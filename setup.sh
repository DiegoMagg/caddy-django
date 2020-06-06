
PROJECT_NAME=$1

if [ ! $1 ]; then
    echo Error: You must provide the project name.
else
    pipenv run django-admin startproject ${PROJECT_NAME} .
    sed -i "s/myproject/${PROJECT_NAME}/g" ./myenv.env ./docker-compose.yml
    sed -i 's|project_path|'$(pwd)/$PROJECT_NAME'|g' ./Caddyfile
    sed -i '71,81 d' $(pwd)/${PROJECT_NAME}/settings.py
    tee -a $(pwd)/${PROJECT_NAME}/settings.py << END

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('POSTGRES_HOST'),
        'POST': 5432,
    },
}
END
    clear
    echo Success!
    echo Now run docker-compose up --build
    sleep 5
    rm ./setup.sh
fi
