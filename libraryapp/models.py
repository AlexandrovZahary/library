from django.db import models
from django.contrib.auth.models import AbstractUser


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=10000)
    author = models.CharField(max_length=1000)
    year_of_publication = models.IntegerField()
    genre = models.CharField(default="Other", max_length=100, choices=(
        ("Action", "Action"),
        ("Adventure", "Adventure"),
        ("Comedy", "Comedy"),
        ("Detective", "Detective"),
        ("Fantasy", "Fantasy"),
        ("Historical", "Historical"),
        ("Historical fiction", "Historical fiction"),
        ("Horror", "Horror"),
        ("Romance", "Romance"),
        ("Satire", "Satire"),
        ("Science fiction", "Science fiction"),
        ("Cyberpunk", "Cyberpunk"),
        ("Speculative", "Speculative"),
        ("Thriller", "Thriller"),
        ("Other", "Other")
    ))
    quantity = models.IntegerField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "book"
        verbose_name_plural = "books"


class User(AbstractUser):
    phone = models.CharField(max_length=11, name="Телефон")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"


class CommentsAndRating(models.Model):
    rating = models.IntegerField()
    comment = models.CharField(max_length=1000)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TakenBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
