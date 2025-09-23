from django.db import models

class Author(models.Model):
    """
    Author model represents a book author.
    Each Author can be associated with multiple Book instances (one-to-many).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model stores information about a book.
    Each Book is linked to one Author via a ForeignKey relationship.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",  # allows reverse lookup: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"