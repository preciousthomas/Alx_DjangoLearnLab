from django.http import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import BasePermission, SAFE_METHODS
from api.models import Book
from .serializers import BookSerializer

"""
Authentication & Permissions:
- TokenAuthentication is enabled (users must login via /api/auth/token/).
- BookViewSet requires authentication for all actions.
- You can customize permissions using DRF’s IsAuthenticated, IsAdminUser,
  or custom rules (see IsAdminOrReadOnly).
"""
def home(request):
    return JsonResponse({"message": "Welcome to the API Project!"})

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from .models import Book

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can CRUD books

    from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  # allow GET
        return request.user and request.user.is_staff

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]

    from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import BookSerializer
from relationship_app.models import Book

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users can CRUD books