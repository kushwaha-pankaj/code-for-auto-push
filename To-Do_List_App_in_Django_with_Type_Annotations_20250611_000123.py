Title: To-Do List App in Django with Type Annotations

```python
# Assuming a Django project is already set up

# Create a new app named 'todo'
# In the terminal run: python manage.py startapp todo

# todo/models.py
from django.db import models

class Task(models.Model):
    """
    Model to represent a Task in the to-do list.
    """
    title: str = models.CharField(max_length=255)
    completed: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

# todo/views.py
from typing import Dict, Any
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Task

def task_list(request) -> HttpResponse:
    """
    View to list all tasks.
    """
    tasks: QuerySet[Task] = Task.objects.all()
    context: Dict[str, Any] = {'tasks': tasks}
    return render(request, 'todo/task_list.html', context)

def add_task(request) -> HttpResponse:
    """
    View to add a new task.
    """
    if request.method == "POST":
        title: str = request.POST.get('title', '')
        if title:
            Task.objects.create(title=title)
        return redirect('task_list')
    return render(request, 'todo/add_task.html')

# urls.py (inside the main Django project's folder)
from django.urls import path
from todo import views as todo_views

urlpatterns = [
    path('', todo_views.task_list, name='task_list'),
    path('add/', todo_views.add_task, name='add_task'),
    # Admin path for Django's built-in admin site (ensure admin app is included in settings)
    path('admin/', admin.site.urls),
]

# todo/templates/todo/task_list.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>To-Do List</title>
</head>
<body>
    <h1>My To-Do List</h1>
    <ul>
    {% for task in tasks %}
        <li>{{ task.title }} - {% if task.completed %}Done{% else %}Pending{% endif %}</li>
    {% endfor %}
    </ul>
    <a href="{% url 'add_task' %}">Add a new task</a>
</body>
</html>
"""

# todo/templates/todo/add_task.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Add Task</title>
</head>
<body>
    <h1>Add a New Task</h1>
    <form method="post">
        {% csrf_token %}
        <input type="text" name="title" placeholder="Task Title">
        <button type="submit">Add Task</button>
    </form>
    <br>
    <a href="{% url 'task_list' %}">Back to Task List</a>
</body>
</html>
"""

# Migrate the database to create the Task model table

# From the terminal, run:
# python manage.py makemigrations todo
# python manage.py migrate

# Run the server to check if everything is working fine
# python manage.py runserver
```

This simple to-do list app in Django uses type annotations to make the code clearer and maintainable. You can expand its functionality by allowing users to delete or modify tasks and adding user authentication.