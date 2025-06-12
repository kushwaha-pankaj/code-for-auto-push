Title: Django Project for QR Code Generation and Scanning with Mobile-First Approach

```python
# settings.py

# Ensure you have Django and required libraries installed
INSTALLED_APPS = [
    ...
    'qr_code_app',  # Add our custom app
    'rest_framework',  # For API development
    "django_qr_code",  # External library for QR code generation
]

# urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('qr_code_app.urls')),  # Include app-specific URLs
]

# qr_code_app/models.py
from django.db import models

# Model to store information about each QR Code
class QRCode(models.Model):
    data = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRCode {self.id} for {self.data}"

# qr_code_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_qr_code.qrcode.utils import QRCodeOptions
from django_qr_code.qrcode.maker import make_qr_code_image
from .models import QRCode

class QRCodeView(APIView):
    """
    API View to handle QR Code generation
    """
    def post(self, request):
        data = request.data.get('data')
        qr_code = QRCode.objects.create(data=data)
        
        # Generate QR code image
        options = QRCodeOptions(size='t', error_correction='M')
        qr_image = make_qr_code_image(data, qr_code_options=options)
        
        response = {
            "qr_code": qr_code.id,
            "qr_image_path": f"/media/qr_codes/{qr_code.id}.png"
        }
        
        # Save the image on the server, you can integrate an external storage as needed
        qr_image.save(f"media/qr_codes/{qr_code.id}.png")
        return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, pk):
        try:
            qr_code = QRCode.objects.get(id=pk)
            response = {
                "data": qr_code.data,
                "created_at": qr_code.created_at
            }
            return Response(response, status=status.HTTP_200_OK)
        except QRCode.DoesNotExist:
            return Response({"error": "QR code not found"}, status=status.HTTP_404_NOT_FOUND)

# qr_code_app/urls.py
from django.urls import path
from .views import QRCodeView

urlpatterns = [
    path('qr-code/', QRCodeView.as_view(), name='qr_code'),
    path('qr-code/<int:pk>/', QRCodeView.as_view(), name='qr_code_detail'),
]

# qr_code_app/templates/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code App</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css">
</head>
<body>
    <div class="container">
        <h1 class="text-center mt-5">Generate QR Code</h1>
        <form id="qrForm" class="mt-4">
            <div class="mb-3">
                <label for="data" class="form-label">Data to encode</label>
                <input type="text" class="form-control" id="data" placeholder="Enter data here">
            </div>
            <button type="submit" class="btn btn-primary">Generate</button>
        </form>
    </div>

    <script>
        const qrForm = document.getElementById('qrForm');
        qrForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const data = document.getElementById('data').value;
            const response = await fetch('/api/qr-code/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ data }),
            });

            if (response.ok) {
                const jsonResponse = await response.json();
                alert('QR Code generated at: ' + jsonResponse.qr_image_path);
            } else {
                alert('Error generating QR Code');
            }
        });
    </script>
</body>
</html>

# Mobile-First responsive design via Bootstrap classes; handle by media queries, etc.
```

In this code, we created a simple Django application for generating QR codes with a mobile-first approach using Bootstrap for responsiveness. This setup includes a simple REST API to generate and retrieve QR code data and server-side image generation using `django_qr_code`.