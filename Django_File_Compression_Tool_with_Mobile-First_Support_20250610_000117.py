Title: Django File Compression Tool with Mobile-First Support

```python
# settings.py
# Standard Django settings with necessary compression libraries

INSTALLED_APPS = [
    #...
    'compressor',  # Django Compressor App
    'myapp',  # The app where the file compression logic is placed
]

# To enable CSS and JS compression
COMPRESS_ENABLED = True
COMPRESS_URL = '/static/'
COMPRESS_ROOT = os.path.join(BASE_DIR, 'static')

# urls.py in myapp
# URL routing configurations for file uploads and compressed file download

from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),  # Main page for file upload
    path('download/<str:file_name>/', views.download_file, name='download_file'),  # Download compressed file
]

# models.py in myapp
# Define a model to store file information

from django.db import models

class UploadedFile(models.Model):
    original_file = models.FileField(upload_to='uploads/')
    compressed_file = models.FileField(upload_to='compressed/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

# views.py in myapp
# Handle file upload, compression, and download

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UploadedFile
from .forms import UploadFileForm
import zipfile
import os

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            
            # Compress the file after saving
            compress_file(uploaded_file)

            return redirect('download_file', file_name=uploaded_file.compressed_file.name)
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def download_file(request, file_name):
    # Serve the compressed file for download
    file_path = os.path.join('compressed', file_name)
    file_abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if os.path.exists(file_abs_path):
        with open(file_abs_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename={file_name}'
            return response
    return HttpResponse('File not found.')

def compress_file(uploaded_file):
    # Simple compression logic using zipfile
    compressed_file_path = os.path.join(settings.MEDIA_ROOT, 'compressed', f'{uploaded_file.original_file.name}.zip')
    
    with zipfile.ZipFile(compressed_file_path, 'w') as zf:
        zf.write(uploaded_file.original_file.path, arcname=os.path.basename(uploaded_file.original_file.name))
    
    # Update the compressed file field in the database
    uploaded_file.compressed_file.name = f'compressed/{os.path.basename(compressed_file_path)}'
    uploaded_file.save()

# forms.py in myapp
# Form for uploading files

from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['original_file']

# templates/upload.html
# HTML Template for mobile-first file upload form

'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Compression Upload</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="{% static 'styles.css' %}">
</head>
<body>
    <div class="container">
        <h1>Upload Your File for Compression</h1>
        <form method="post" enctype="multipart/form-data">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Upload</button>
        </form>
    </div>
</body>
</html>
'''

# static/styles.css
# Basic mobile-first CSS styling

'''
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}

.container {
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}

form {
    display: flex;
    flex-direction: column;
}

button {
    margin-top: 10px;
}
'''
```