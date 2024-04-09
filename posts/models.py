from django.db import models
from django.urls import path
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.TextField(
        'Название группы',
        help_text='Напишите, как будет называться ваша группа'
    )
    slug = models.SlugField(
        'Никнейм вашей группы',
        help_text='Придумайте сокращенное название вашей группы'
    )
    description = models.TextField(
        'Описание группы',
        help_text='Добавьте описание для вашей группы'
    )

    def __str__(self):
        return self.title


class Tag(CreatedModel):
    name = models.TextField(
        'Наименование хэштега'
    )

    def __str__(self):
        return self.name


class Post(CreatedModel):
    text = models.TextField(
        'Текст поста',
        help_text='Напишите текст, который хотите опубликовать'
    )

    group = models.ForeignKey(
        Group,
        related_name='posts',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Группа',
        help_text='Выберите группу'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )

    # Поле для картинки (необязательное)
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    tag = models.ManyToManyField(
        Tag,
        through='TagPost'
    )

    def __str__(self):
        # выводим текст поста
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        verbose_name='Пост',
        on_delete=models.CASCADE,
    )

    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )

    text = models.TextField(
        'Комментарий',
        help_text='Напишите комментарий',
    )

    def __str__(self):
        return self.text[:15]


class TagPost(CreatedModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.post}'
