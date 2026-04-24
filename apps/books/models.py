from django.db import models


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    published_year = models.IntegerField(null=True, blank=True)
    stock = models.IntegerField(default=0)
    description = models.TextField(null=True, blank=True)
    cover_url = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return f"{self.title} — {self.author}"
