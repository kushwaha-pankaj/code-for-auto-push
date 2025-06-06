
Title: Django To-Do List App

```python
# tasks/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)  # Task title
    completed = models.BooleanField(default=False)  # Task completion status

    def __str__(self):
        return self.title  # String representation for the task

# tasks/views.py
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    tasks = Task.objects.all()  # Get all tasks
    return render(request, 'tasks/task_list.html', {'tasks': tasks})  # Render task list template with tasks

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()  # Save new task to database
            return redirect('task_list')  # Redirect to task list view
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})  # Render add task form

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()  # Delete the selected task
    return redirect('task_list')  # Redirect back to task list view

# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task  # Form model
        fields = ['title', 'completed']  # Fields in the form

# tasks/templates/tasks/task_list.html
{% extends 'base_generic.html' %}

{% block content %}
  <h2>Your To-Do List</h2>
  <ul>
    {% for task in tasks %}
      <li>{{ task.title }} 
        {% if task.completed %}(Completed){% endif %}
        <a href="{% url 'delete_task' task.id %}">Delete</a>
      </li>
    {% endfor %}
  </ul>
  <a href="{% url 'add_task' %}">Add a new task</a>
{% endblock %}

# tasks/templates/tasks/add_task.html
{% extends 'base_generic.html' %}

{% block content %}
  <h2>Add a New Task</h2>
  <form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Add Task</button>
  </form>
  <a href="{% url 'task_list' %}">Back to list</a>
{% endblock %}

# tasks/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # Task list view
    path('add/', views.add_task, name='add_task'),  # Add task view
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # Delete task view
]

# project/urls.py (assuming 'tasks' is the name of the app)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  # Include tasks app URLs
]

# To set up a new project and app, create the following:
# django-admin startproject project
# python manage.py startapp tasks

# Don't forget to add 'tasks' to INSTALLED_APPS in the settings.py of your project.

# settings.py
INSTALLED_APPS = [
    # ...
    'tasks',  # Register the tasks app
    # ...
]

# After setting everything up, run the following commands to migrate changes and start the server:
# python manage.py makemigrations tasks
# python manage.py migrate
# python manage.py runserver
```

This example illustrates a simple Django To-Do List application following the MVC architectural pattern. Tasks are stored in a database, with the application offering functionality to add and delete tasks via web forms.