FROM python:3

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install django djangorestframework django-cors-headers mysqlclient

VOLUME [ "/app" ]

EXPOSE 8000
CMD [ "python", "manage.py", "runserver", "app:8000" ]