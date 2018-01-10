from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=64, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)

class Recommendation(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    book_list = models.ManyToManyField(User)
