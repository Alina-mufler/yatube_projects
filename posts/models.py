from django.db import models
from django.urls import path
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.TextField()
    slug = models.SlugField()
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    group = models.ForeignKey(
        Group,
        related_name='groups',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )



