Title: Django To-Do List App with Database Support

```python
# Import necessary Django modules
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from django.urls import path
from django import forms

# Define the Task model with an optimized table structure for performance
class Task(models.Model):
    # Primary key field is automatically added by Django unless specified otherwise.
    task_text = models.CharField(max_length=255, db_index=True) # Adding an index for faster search performance
    completed = models.BooleanField(default=False)

    # String representation of the model instance
    def __str__(self):
        return self.task_text

# Create a ModelForm for Task to handle form operations and validation
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task_text', 'completed']

# List view of the tasks
def task_list(request):
    # Retrieve all tasks and order them by completion status and text for better readability
    tasks = Task.objects.all().order_by('completed', 'task_text')
    form = TaskForm()
    return render(request, 'task_list.html', {'tasks': tasks, 'form': form})

# Add a new task to the to-do list
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save() # Save the new task to the database
    return redirect('task_list')

# Update the status of a task
def toggle_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

# Delete a task from the to-do list
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('task_list')

# Define URL patterns for different actions
urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('toggle/<int:task_id>/', toggle_task, name='toggle_task'),
    path('delete/<int:task_id>/', delete_task, name='delete_task'),
]

# Basic HTML template for task list (task_list.html)
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>To-Do List</title>
</head>
<body>
    <h1>To-Do List</h1>
    <form method="post" action="{% url 'add_task' %}">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Add Task</button>
    </form>
    <ul>
        {% for task in tasks %}
            <li>
                <span style="text-decoration: {{ 'line-through' if task.completed else 'none' }};">
                    {{ task.task_text }}
                </span>
                <a href="{% url 'toggle_task' task.id %}">{{ 'Undo' if task.completed else 'Complete' }}</a>
                <a href="{% url 'delete_task' task.id %}">Delete</a>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

# Additionally, configure settings in your Django project's settings.py: 
# DATABASES, INSTALLED_APPS (add the app name where this code resides), etc.
```

This simple Django to-do app efficiently handles adding, toggling, and deleting tasks. It uses a SQLite database by default, which can be configured to use other options depending on the project's needs. The use of Django's ORM allows for optimized database interactions and performance.