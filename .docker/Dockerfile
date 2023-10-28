FROM python:3

WORKDIR /app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade pip
RUN pip install django djangorestframework django-cors-headers mysqlclient Pillow 

# install mysqlclient

# bootstrap
RUN django-admin startproject mysite


VOLUME ["/app"] 

EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "app:8000"]
