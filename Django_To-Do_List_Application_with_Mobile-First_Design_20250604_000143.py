Title: Django To-Do List Application with Mobile-First Design

```python
# settings.py
# Import necessary modules
import os
from pathlib import Path

# Set base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define installed applications
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'todo',  # Custom app for to-do functionality
]

# Define middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configure the database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Specify static files directory
STATIC_URL = '/static/'

# Define URL configuration
ROOT_URLCONF = 'myproject.urls'

# Define template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Specify WSGI application
WSGI_APPLICATION = 'myproject.wsgi.application'

# Define secret key
SECRET_KEY = 'your-secret-key-here'

# Toggle debug mode
DEBUG = True

# Set allowed hosts
ALLOWED_HOSTS = []

# Specify default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

```python
# models.py
from django.db import models

# Define a task model
class Task(models.Model):
    title = models.CharField(max_length=255)  # Task title
    completed = models.BooleanField(default=False)  # Completion status

    def __str__(self):
        # Return the title when a task is printed
        return self.title
```

```python
# views.py
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

# Display list of tasks
def index(request):
    tasks = Task.objects.all()  # Retrieve all tasks
    form = TaskForm()  # Form for new tasks
    context = {'tasks': tasks, 'form': form}  # Context passed to template
    return render(request, 'todo/index.html', context)  # Render response

# Add new task
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)  # Bound form
        if form.is_valid():  # Check form validity
            form.save()  # Save in database
            return redirect('index')  # Redirect after saving
    else:
        form = TaskForm()
    
    context = {'form': form}
    return render(request, 'todo/add.html', context)

# Remove task
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)  # Retrieve specific task
    task.delete()  # Delete task
    return redirect('index')  # Redirect back to task list
```

```python
# forms.py
from django import forms
from .models import Task

# Define task form
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # Use Task model
        fields = ['title']  # Include only the title field in the form
```

```django
<!-- templates/todo/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do List</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div class="container">
        <h1>To-Do List</h1>
        <form method="post" action="{% url 'add_task' %}">
            {% csrf_token %}
            {{ form }}
            <button type="submit">Add Task</button>
        </form>
        <ul>
            {% for task in tasks %}
                <li>
                    <span>{{ task.title }}</span>
                    <a href="{% url 'delete_task' task.id %}">Delete</a>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
```

```python
# urls.py within the "todo" app
from django.urls import path
from . import views

# Define URL patterns
urlpatterns = [
    path('', views.index, name='index'),  # Home page with list of tasks
    path('add/', views.add_task, name='add_task'),  # Add new tasks
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Delete tasks
]

# urls.py at project level
from django.contrib import admin
from django.urls import path, include

# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),  # Include app-level URLs
]
```

```css
/* static/css/style.css */
body {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 500px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

h1 {
    text-align: center;
}

ul {
    list-style: none;
    padding: 0;
}

li {
    background: #eee;
    margin: 5px 0;
    padding: 10px;
    display: flex;
    justify-content: space-between;
}

button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
}

button:hover {
    background-color: #45a049;
}
```

This code implements a simple Django to-do list application with a mobile-first design. The app includes a list of tasks, as well as the ability to add and delete tasks.