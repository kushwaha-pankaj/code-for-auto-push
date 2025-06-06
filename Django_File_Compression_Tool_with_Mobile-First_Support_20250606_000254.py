Title: Django File Compression Tool with Mobile-First Support

```python
# Install Django and required packages by running:
# pip install django pillow

# First, create a Django project and app. Use the following commands:
# django-admin startproject file_compressor
# cd file_compressor
# python manage.py startapp compression

# settings.py
# Add 'compression' to the list of INSTALLED_APPS

INSTALLED_APPS = [
    ...
    'compression',
]

# models.py
from django.db import models

# Create a FileUpload model to handle uploaded files
class FileUpload(models.Model):
    uploaded_file = models.FileField(upload_to='uploads/')

# forms.py
from django import forms
from .models import FileUpload

# Create a form to upload files
class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['uploaded_file']

# views.py
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from zipfile import ZipFile
import os
from django.conf import settings

# Handle file upload and compression
def upload_and_compress(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save()  # Save the uploaded file
            compress_file(file_instance.uploaded_file.path)  # Compress the uploaded file
            return redirect('upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'upload.html', {'form': form})

# Create a zipped version of the uploaded file
def compress_file(file_path):
    base_name = os.path.splitext(file_path)[0]
    zip_file_path = f"{base_name}.zip"
    with ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(file_path, arcname=os.path.basename(file_path))

# urls.py in compression app
from django.urls import path
from . import views

# Define URL patterns for the app
urlpatterns = [
    path('', views.upload_and_compress, name='upload_and_compress'),
    path('success/', views.upload_success, name='upload_success'),
]

# views.py (additional success view function)
def upload_success(request):
    return render(request, 'success.html')

# templates/upload.html
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload and Compress File</title>
    <!-- Mobile-first design using a simple style -->
    <style>
        body { font-family: Arial, sans-serif; }
        .container { width: 90%; max-width: 600px; margin: auto; }
        form { display: flex; flex-direction: column; }
    </style>
</head>
<body>
<div class="container">
    <h1>Upload File</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Upload and Compress</button>
    </form>
</div>
</body>
</html>
'''

# templates/success.html
'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Successful</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 40px; }
    </style>
</head>
<body>
    <h1>File Uploaded and Compressed Successfully!</h1>
    <a href="{% url 'upload_and_compress' %}">Upload Another File</a>
</body>
</html>
'''

# Run the Django development server to test:
# python manage.py runserver

# This Django app allows users to upload a file, which is then compressed into a ZIP file.
# The design is mobile-first with a simple responsive layout. 
# Make sure to handle file storage and cleanup based on your needs in a production environment.
```