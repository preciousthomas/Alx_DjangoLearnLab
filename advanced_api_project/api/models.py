from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)  # ✅ required field

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)             # ✅ required field
    publication_year = models.IntegerField()             # ✅ required field
    author = models.ForeignKey(
        Author,
        related_name="books",
        on_delete=models.CASCADE
    )  # ✅ one-to-many relationship

    def __str__(self):
        return f"{self.title} ({self.publication_year})"