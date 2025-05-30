Title: Building a RESTful API with Django Rest Framework and Error Handling

```python
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db import models
from rest_framework import routers
from django.urls import path, include

# --- Models ---
class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

# --- Serializers ---
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']

# --- ViewSets ---
class ItemViewSet(viewsets.ViewSet):

    def list(self, request):
        """Handle GET requests for retrieving all items"""
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST requests for creating an item"""
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for retrieving a specific item by id"""
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for updating an item"""
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for deleting an item"""
        item = get_object_or_404(Item, pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --- API View for handling errors ---
@api_view(['POST'])
def handle_errors(request):
    """A mock endpoint to demonstrate error handling in action"""
    if 'name' not in request.data:
        return JsonResponse({'error': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'message': 'Success'}, status=status.HTTP_200_OK)

# --- Routers ---
router = routers.DefaultRouter()
router.register(r'items', ItemViewSet, basename='item')

# --- URL Patterns ---
urlpatterns = [
    path('', include(router.urls)),
    path('handle-errors/', handle_errors),
]
```

In this example, we have set up a simple RESTful API using Django Rest Framework:
1. **Model**: Defines an `Item` with `name` and `description`.
2. **Serializer**: Converts the `Item` model instances to JSON.
3. **ViewSet**: Manages CRUD operations for `Item`. Graceful error handling is evident, such as returning 400 errors with descriptive validation messages.
4. **Error Handling View**: A mock endpoint demonstrating JSON-based error messages.
5. **Routers** and **URL patterns** tie everything together, ready for API use.