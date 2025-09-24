from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
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
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']  # filtering
    search_fields = ['title', 'author']  # searching
    ordering_fields = ['title', 'publication_year']  # ordering
    ordering = ['title']  # default ordering
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend


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
    permission_classes = [permissions.IsAuthenticated]

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
    # Filtering: /books/?author=John&publication_year=2020
# Searching: /books/?search=Python
# Ordering: /books/?ordering=title or /books/?ordering=-publication_year