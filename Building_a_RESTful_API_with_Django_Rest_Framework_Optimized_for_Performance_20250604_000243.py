Title: Building a RESTful API with Django Rest Framework Optimized for Performance

```python
# Import necessary libraries and modules
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.db import models
from rest_framework import routers, serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Define a simple model for demonstration
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

# Serializer to convert model instances to JSON and vice versa
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']

# Custom pagination class to optimize data transfer and response time
class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

# ViewSet to handle CRUD operations for Item model
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('id')
    serializer_class = ItemSerializer
    pagination_class = CustomPagination  # Apply custom pagination

    # Optionally, override the list method for additional performance tweaking if needed
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Possible enhancement: add caching mechanisms here for performance
        return response

# Router to automatically generate URL patterns for the ViewSet
router = routers.DefaultRouter()
router.register(r'items', ItemViewSet)

# Application URL configuration
urlpatterns = [
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# settings.py (assuming production settings are separate; minimal setup shown here for context)
# Optimize database query and connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',  # Set to the actual database host
        'PORT': '5432',
        'CONN_MAX_AGE': 600  # Persistent connections
    }
}

# Middleware for performance optimization
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Additional middleware for compression and caching could be added here
]

# Other settings and configurations are assumed pre-configured for project-specific requirements

# Main entry point for the Django application
if __name__ == "__main__":
    import os
    import django

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
    django.setup()

    from django.core.management import execute_from_command_line

    execute_from_command_line()
```

This code builds a simple and performant RESTful API using Django and the Django Rest Framework. The code includes basic CRUD operations for an `Item` model and uses pagination to optimize performance. It also outlines some database and middleware configurations to enhance performance further.