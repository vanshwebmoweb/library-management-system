# Library Management System

A REST API built with Django REST Framework.

## Features
- JWT Authentication
- Custom User Model
- Book, Author, Category, BorrowRecord models
- Different view types (Generic, APIView, ModelViewSet)
- Custom Permissions
- Validations in Serializers
- Pagination

## Setup

### Install dependencies
pip install -r requirements.txt

### Run migrations
python manage.py makemigrations
python manage.py migrate

### Create superuser
python manage.py createsuperuser

### Run server
python manage.py runserver