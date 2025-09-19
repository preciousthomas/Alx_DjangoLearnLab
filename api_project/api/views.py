from django.http import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
from api.models import Book
from .serializers import BookSerializer

def home(request):
    return JsonResponse({"message": "Welcome to the API Project!"})

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer