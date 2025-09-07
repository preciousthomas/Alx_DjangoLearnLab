import os
import sys
import django

# Ensure the project root (where manage.py lives) is on the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


# 1. Query all books by a specific author
def get_books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


# 2. List all books in a library
def get_books_in_library(library_name):
    return Book.objects.filter(libraries__name=library_name)


# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    return Librarian.objects.filter(library__name=library_name).first()


if __name__ == "__main__":
    # Example usage (replace names with real values from your DB)
    print("📚 Books by Author:", list(get_books_by_author("John Doe")))
    print("📚 Books in Library:", list(get_books_in_library("Central Library")))
    print("👨‍🏫 Librarian of Library:", get_librarian_for_library("Central Library"))