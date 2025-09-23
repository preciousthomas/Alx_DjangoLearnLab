from django.db import models

# Create your models here.
from django.db import models

class Author(models.Model):
    """
    Author model represents a book author.
    Each Author can have multiple related Books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a book with a title, 
    its publication year, and a foreign key 
    linking to the Author model.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',  # used in nested serialization
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"