from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to the API Project!"})

from rest_framework import generics
from api_project.relationship_app.models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer