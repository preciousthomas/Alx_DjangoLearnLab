import os
import django

# Setup Django environment so this script can run standalone
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from relationship_app.models import Author, Book, Library, Librarian


def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        return books
    except Author.DoesNotExist:
        return []


def list_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return []


def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None


if __name__ == "__main__":
    # Example usage
    books_by_author = get_books_by_author("John Doe")
    print("Books by John Doe:", [book.title for book in books_by_author])

    library_books = list_books_in_library("Central Library")
    print("Books in Central Library:", [book.title for book in library_books])

    librarian = get_librarian_for_library("Central Library")
    if librarian:
        print("Librarian of Central Library:", librarian.name)
    else:
        print("No librarian found for Central Library")