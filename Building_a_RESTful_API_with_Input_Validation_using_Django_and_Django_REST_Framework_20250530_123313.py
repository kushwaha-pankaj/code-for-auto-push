Title: Building a RESTful API with Input Validation using Django and Django REST Framework

```python
# First, we need to create a new Django project and app.
# Run the following commands in your terminal to set up the environment.

# $ django-admin startproject myapi
# $ cd myapi
# $ python manage.py startapp myapp

# Now, we will add 'rest_framework' and 'myapp' to the INSTALLED_APPS in myapi/settings.py.

INSTALLED_APPS = [
    ...
    'rest_framework',
    'myapp',
]

# We'll define a simple model in myapp/models.py.

from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# Next, we'll create a serializer for the Item model in myapp/serializers.py.

from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']
    
    # Adding input validation
    def validate_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Name must contain only alphabetic characters.")
        return value

# Now, let's create some views in myapp/views.py.

from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer

# A simple ViewSet for viewing and editing items.
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# We need to configure our URL routing.
# In myapp/urls.py, include the following:

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

# Include myapp URLs in the main project myapi/urls.py.

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# Finally, apply the database migrations to create the tables for our models.

# $ python manage.py makemigrations myapp
# $ python manage.py migrate

# Run the development server to test the API.

# $ python manage.py runserver

# You can now access the API at http://127.0.0.1:8000/items/
# Try creating an item using a REST client like Postman or curl with valid and invalid data to see the input validation in action.
```