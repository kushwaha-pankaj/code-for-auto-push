Title: Django Application for Generating and Scanning QR Codes

```python
# settings.py
# Ensure you have the required libraries installed:
# `pip install pillow qrcode opencv-python-headless`

INSTALLED_APPS = [
    ...
    'qr_code_app',  # Add the app to your installed apps
]

# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('qr_code_app.urls')),  # Include urls from the QR code app
]

# qr_code_app/models.py
from django.db import models

class QRCode(models.Model):
    # Model to store information about the QR codes
    name = models.CharField(max_length=100)
    data = models.CharField(max_length=255)
    qr_image = models.ImageField(upload_to='qr_codes/')

    def __str__(self):
        return self.name

# qr_code_app/views.py
import qrcode
from django.shortcuts import render, redirect
from .models import QRCode
from django.core.files.base import ContentFile
import cv2
from django.http import HttpResponse
import numpy as np

def generate_qr_code(request):
    # View to generate a QR code
    if request.method == 'POST':
        name = request.POST['name']
        data = request.POST['data']

        qr = qrcode.make(data)
        qr_image = ContentFile(qr.tobytes(), name=f"{name}.png")

        QRCode.objects.create(name=name, data=data, qr_image=qr_image)
        return redirect('qr_list')

    return render(request, 'qr_code_app/generate.html')

def qr_list(request):
    # View to list all generated QR codes
    qr_codes = QRCode.objects.all()
    return render(request, 'qr_code_app/list.html', {'qr_codes': qr_codes})

def scan_qr_code(request):
    # Function to scan a QR code from an image
    if request.method == 'POST':
        file = request.FILES['qr_image']
        img_array = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        
        detector = cv2.QRCodeDetector()
        data, _, _ = detector.detectAndDecode(img)
        
        return HttpResponse(f"Scanned Data: {data}")

    return render(request, 'qr_code_app/scan.html')

# qr_code_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_qr_code, name='generate_qr_code'),
    path('list/', views.qr_list, name='qr_list'),
    path('scan/', views.scan_qr_code, name='scan_qr_code'),
]

# qr_code_app/templates/qr_code_app/generate.html
# HTML template to generate QR codes
"""
<!DOCTYPE html>
<html>
<head>
    <title>Generate QR Code</title>
</head>
<body>
    <h1>Generate QR Code</h1>
    <form method="post">
        {% csrf_token %}
        <input type="text" name="name" placeholder="Enter Name" required><br>
        <input type="text" name="data" placeholder="Enter Data" required><br>
        <button type="submit">Generate</button>
    </form>
    <a href="{% url 'qr_list' %}">View QR Codes</a>
</body>
</html>
"""

# qr_code_app/templates/qr_code_app/list.html
# HTML template to list QR codes
"""
<!DOCTYPE html>
<html>
<head>
    <title>QR Code List</title>
</head>
<body>
    <h1>QR Codes</h1>
    <ul>
        {% for qr in qr_codes %}
            <li>{{ qr.name }} - <img src="{{ qr.qr_image.url }}" alt="{{ qr.name }}"></li>
        {% endfor %}
    </ul>
    <a href="{% url 'generate_qr_code' %}">Generate New QR Code</a><br>
    <a href="{% url 'scan_qr_code' %}">Scan QR Code</a>
</body>
</html>
"""

# qr_code_app/templates/qr_code_app/scan.html
# HTML template to scan QR codes
"""
<!DOCTYPE html>
<html>
<head>
    <title>Scan QR Code</title>
</head>
<body>
    <h1>Scan QR Code</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <input type="file" name="qr_image" accept="image/*" required><br>
        <button type="submit">Scan</button>
    </form>
</body>
</html>
"""
```

The above code provides a simple implementation of a Django application that allows users to generate and scan QR codes. The application is divided into several components following a modular design, adhering to clean and simple practices.