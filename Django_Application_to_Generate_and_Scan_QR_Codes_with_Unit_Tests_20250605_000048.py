Title: Django Application to Generate and Scan QR Codes with Unit Tests

```python
# myproject/settings.py
"""
Django settings for myproject.
Adjust the necessary settings based on your database choice and other configurations.
"""

# ...

# Add 'qrcode' app to INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'qrcode',
]

# ...

# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr/', include('qrcode.urls')),
]

# qrcode/apps.py
from django.apps import AppConfig

class QrcodeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qrcode'

# qrcode/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_qr_code, name='generate_qr_code'),
    path('scan/', views.scan_qr_code, name='scan_qr_code'),
]

# qrcode/views.py
from django.http import JsonResponse
import qrcode
import cv2
import numpy as np
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def generate_qr_code(request):
    # Generate a QR Code for the given data
    data = request.GET.get('data', 'default')
    qr_img = qrcode.make(data)
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    buffer.seek(0)
    qr_file = InMemoryUploadedFile(buffer, None, 'qr.png', 'image/png', buffer.tell(), None)
    return JsonResponse({'message': 'QR Code generated', 'file': qr_file.name})

def scan_qr_code(request):
    # Scan a QR Code and return the encoded data
    file = request.FILES['file']
    np_img = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)
    if data:
        return JsonResponse({'data': data})
    return JsonResponse({'error': 'No QR code detected'}, status=400)

# qrcode/tests.py
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import qrcode
from io import BytesIO

class QRCodeTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_generate_qr_code(self):
        response = self.client.get('/qr/generate/', {'data': 'test'})
        self.assertEqual(response.status_code, 200)
        # Check if the response contains the file name
        self.assertIn('qr.png', response.json().get('file', ''))

    def test_scan_qr_code(self):
        # Create a QR code to test scanning
        qr_img = qrcode.make('test_data')
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        buffer.seek(0)
        qr_file = SimpleUploadedFile('qr.png', buffer.read(), content_type='image/png')
        
        response = self.client.post('/qr/scan/', {'file': qr_file})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('data'), 'test_data')
```

This Django application demonstrates generating and scanning QR codes. The `generate_qr_code` view creates a QR code based on query parameters, while the `scan_qr_code` view decodes a sent QR image file. Unit tests ensure both functionalities work correctly. Adjust the settings in `myproject/settings.py` to fit your Django setup.