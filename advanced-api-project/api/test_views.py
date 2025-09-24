from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.admin = User.objects.create_superuser(username="admin", password="adminpass123")

        # Create sample books
        self.book1 = Book.objects.create(title="Book One", author="Author A", publication_year=2020)
        self.book2 = Book.objects.create(title="Book Two", author="Author B", publication_year=2021)

        # Endpoint URL
        self.list_url = reverse("book-list")  # assumes you used DefaultRouter with BookViewSet

    def test_list_books(self):
        """Test retrieving list of books (public read access)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_unauthenticated(self):
        """Test that unauthenticated users cannot create books."""
        data = {"title": "Book Three", "author": "Author C", "publication_year": 2022}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Test authenticated user can create a book."""
        self.client.login(username="testuser", password="testpass123")
        data = {"title": "Book Three", "author": "Author C", "publication_year": 2022}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        """Test updating a book by authenticated user."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("book-detail", args=[self.book1.id])
        data = {"title": "Updated Book", "author": "Author A", "publication_year": 2020}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book_non_admin(self):
        """Test normal user cannot delete a book if restricted by permissions."""
        self.client.login(username="testuser", password="testpass123")
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED])

    def test_delete_book_admin(self):
        """Test admin can delete a book."""
        self.client.login(username="admin", password="adminpass123")
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        response = self.client.get(self.list_url, {"author": "Author A"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Author A")

    def test_search_books_by_title(self):
        """Test searching books by title."""
        response = self.client.get(self.list_url, {"search": "Book One"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year(self):
        """Test ordering books by publication_year."""
        response = self.client.get(self.list_url, {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["publication_year"], 2021)