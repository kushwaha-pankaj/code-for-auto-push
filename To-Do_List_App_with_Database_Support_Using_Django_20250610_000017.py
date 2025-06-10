Title: To-Do List App with Database Support Using Django

```python
# Install Django if you haven't already by running: pip install django

# 1. Setting Up the Django Project

# Create a new Django project
# Run in terminal: django-admin startproject todo_project

# Navigate inside the project directory
# cd todo_project

# Create a new Django app
# Run in terminal: python manage.py startapp todo

# 2. Updating the Models

# In todo/models.py, define the database model for a Task.

from django.db import models

class Task(models.Model):
    """
    Model to represent a Task in the to-do list app.
    Attributes:
        title (str): The title of the task.
        description (str): A brief description of the task.
        is_complete (bool): Status flag if the task is completed.
        created_date (datetime): The date and time the task was created.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_complete = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the Task object.
        """
        return self.title

# 3. Registering the Model with Admin

# In todo/admin.py, register the Task model to manage through Django admin.

from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin panel configuration for Task model.
    """
    list_display = ('title', 'is_complete', 'created_date')
    list_filter = ('is_complete', 'created_date')
    search_fields = ('title', )

# 4. Add the App to the Project Settings

# In todo_project/settings.py, add the 'todo' app to INSTALLED_APPS.

INSTALLED_APPS = [
    ...,
    'todo',  # Add the todo app here
]

# 5. Creating the Views

# In todo/views.py, create views for listing, creating, and updating tasks.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

def task_list(request):
    """
    View to list all tasks.
    """
    tasks = Task.objects.all()
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def task_create(request):
    """
    View to create a new task.
    """
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todo/task_form.html', {'form': form})

def task_update(request, pk):
    """
    View to update an existing task.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todo/task_form.html', {'form': form})

# 6. Creating Forms

# In todo/forms.py, define a form for creating and updating tasks.

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    Form to facilitate creating and updating tasks.
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'is_complete']

# 7. Creating the URLs

# In todo/urls.py, configure URLs for the views.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('new/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
]

# 8. Project URL Configuration

# In todo_project/urls.py, include the todo app URLs.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls')),
]

# 9. Creating Templates

# Create HTML templates for listing and managing tasks.
# Create a directory named 'templates/todo' inside the 'todo' app.

# Inside 'todo/templates/todo/task_list.html', list all tasks.
"""
<!DOCTYPE html>
<html>
<head>
    <title>To-Do List</title>
</head>
<body>
    <h1>To-Do List</h1>
    <a href="{% url 'task_create' %}">Add New Task</a>
    <ul>
        {% for task in tasks %}
            <li>
                {{ task.title }} - {% if task.is_complete %}Completed{% else %}Pending{% endif %}
                <a href="{% url 'task_update' task.pk %}">Edit</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Inside 'todo/templates/todo/task_form.html', create/edit a task.
"""
<!DOCTYPE html>
<html>
<head>
    <title>Task Form</title>
</head>
<body>
    <h1>{{ form.instance.pk|yesno:"Edit,Add" }} Task</h1>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
</body>
</html>
"""

# 10. Running Database Migrations

# Run the migrations to create database tables for the Task model.
# python manage.py makemigrations todo
# python manage.py migrate

# 11. Running the Server

# Start the Django development server and access the application.
# python manage.py runserver

# Access the application at: http://127.0.0.1:8000
```

This code snippet sets up a basic Django project for a to-do list application, complete with database integration, simple views, and templates. It uses Django's functionality to create a user-friendly interface for managing tasks. Each section is documented with docstring comments to describe the purpose and intent of the code.