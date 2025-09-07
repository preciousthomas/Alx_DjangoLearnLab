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
    # Style 1: get author then list their books
    author = Author.objects.get(name=author_name)
    books_via_relation = author.books.all()

    # Style 2: filter directly using author instance
    books_via_filter = Book.objects.filter(author=author)

    return books_via_relation, books_via_filter


# 2. List all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)

    # Style 1: via reverse OneToOne relation
    librarian_via_relation = library.librarian

    # Style 2: explicitly querying Librarian by library
    librarian_via_filter = Librarian.objects.get(library=library)

    return librarian_via_relation, librarian_via_filter


if __name__ == "__main__":
    books1, books2 = get_books_by_author("John Doe")
    print("📚 Books by Author (via relation):", list(books1))
    print("📚 Books by Author (via filter):", list(books2))
    print("📚 Books in Library:", list(get_books_in_library("Central Library")))
    lib1, lib2 = get_librarian_for_library("Central Library")
    print("👨‍🏫 Librarian of Library (via relation):", lib1)
    print("👨‍🏫 Librarian of Library (via filter):", lib2)