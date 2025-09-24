from rest_framework import generics
from rest_framework import permissions
from .models import Book
from .serializers import BookSerializer

# ---------------------------
# List all books (public)
# ---------------------------
class BookListView(generics.ListAPIView):
    """
    ListView: Returns all books.
    - Accessible by anyone (authenticated or not).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------
# Retrieve one book by ID (public)
# ---------------------------
class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView: Returns a single book by ID.
    - Accessible by anyone.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# ---------------------------
# Create a new book (authenticated only)
# ---------------------------
class BookCreateView(generics.CreateAPIView):
    """
    CreateView: Allows authenticated users to add a new book.
    - Validates input via BookSerializer.
    """
queryset = Book.objects.all()
serializer_class = BookSerializer
permission_classes = [permissions.IsAuthenticatedOrReadOnly]

def perform_create(self, serializer):
    """
    Custom behavior:
    - Hook called when saving a new object.
    - Can add extra logic here (logging, attaching user, etc.).
    """
    serializer.save()


# ---------------------------
# Update an existing book (authenticated only)
# ---------------------------
class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView: Allows authenticated users to update an existing book.
    - Uses validation from BookSerializer.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom behavior:
        - Hook called when updating an object.
        - Useful for applying business rules.
        """
        serializer.save()


# ---------------------------
# Delete a book (authenticated only)
# ---------------------------
class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView: Allows authenticated users to delete a book.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]