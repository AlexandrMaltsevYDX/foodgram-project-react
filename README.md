## TECH USED:

[![Python](https://img.shields.io/badge/-Python-464646?style=for-the-badge&logo=Python&logoColor=FFFFF&color=692784)](https://www.python.org/)

[![Django](https://img.shields.io/badge/-Django-464646?style=for-the-badge&logo=Django&logoColor=FFFFF&color=692784)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=for-the-badge&logo=Django%20REST%20Framework&logoColor=FFFFF&color=692784)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=for-the-badge&color=692784)](https://jwt.io/)

[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=for-the-badge&logo=NGINX&logoColor=FFFFF&color=692784)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=for-the-badge&logo=gunicorn&logoColor=FFFFF&color=692784)](https://gunicorn.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=for-the-badge&logo=PostgreSQL&logoColor=FFFFF&color=692784)](https://www.postgresql.org/)

[![Docker](https://img.shields.io/badge/-Docker-464646?style=for-the-badge&logo=Docker&logoColor=FFFFF&color=692784)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=for-the-badge&logo=Docker&logoColor=FFFFF&color=692784)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=for-the-badge&logo=Docker&logoColor=FFFFF&color=692784)](https://www.docker.com/products/docker-hub)

[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=for-the-badge&logo=GitHub%20actions&logoColor=FFFFF&color=692784)](https://github.com/features/actions)

[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=for-the-badge&logo=Yandex.Cloud&logoColor=FFFFF&color=692784)](https://cloud.yandex.ru/)



# FOODGRAM
http://158.160.56.76/signin/


# How to install
### For remote
ssh name@0.0.0.0
mkdir projects/fodgram/

## Clone repository to fodgram if remote or just clone it
```
git clone https://github.com/AlexandrMaltsevYDX/foodgram-project-react.git
```


## create .env file
```
touch foodgram/infra/.env
```

```
DEBUG =True # For localhost
DEBUG =True # For remote
SECRET_KEY = SECRET_KEY
ALLOWED_HOSTS =127.0.0.1 # For localhost
ALLOWED_HOSTS =ALLOWED_HOSTS # For remote
DB_ENGINE =django.db.backends.postgresql
DB_NAME = postgres
POSTGRES_USER = postgres
POSTGRES_PASSWORD = postgres
DB_HOST= db
DB_PORT= 5432
```
##

## start docker from infra
```
sudo docker compose up
```


# Alexandr Maltsev