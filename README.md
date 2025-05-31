# Django_Internship_Project

# Django Internship Project: To-Do List Web App

This project is a simple, functional Django-based web application for managing personal to-do tasks. Users can register, log in, and manage their task list via a clean interface. This project was developed as part of an internship program to demonstrate core Django competencies such as authentication, models, views, and templates.

## Features

- ✅ User authentication (sign up, login, logout)   
- ✅ Custom user model integration  
- ✅ SQLite database backend  
- ✅ Minimal and clean UI using Django templating  

## Tech Stack

- **Python** 3.10+  
- **Django** 5.2.1  
- **Database**: SQLite (default for development)

## Getting Started

### Clone the Repository
  ```bash
    git clone https://github.com/bransen36/Django_Internship_Project.git
    cd Django_Internship_Project
  ```
### Set up a Virtual Environment
  ```bash
   python -m venv venv
   venv\Scripts\activate  # On Linux: source venv/vin/activate
  ```
### Install Dependencies
  ```bash
    pip install django
  ```
### Apply Database Migrations
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```
### Create a Superuser (Optional)
  ```bash
  python manage.py createsuperuser
  ```
### Run the Development Server
  ```bash
  python manage.py runserver
  ```
Open your browser and go to:
http://127.0.0.1:8000
