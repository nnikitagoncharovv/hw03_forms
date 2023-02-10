from django.contrib.auth import get_user_model

from django.db import models


User = get_user_model()


class Group(models.Model):
    """Модель для групп."""

    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=150,
        unique=True,
        verbose_name='Элементы')
    description = models.TextField(
        max_length=400,
        verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель для постов"""

    text = models.TextField(
        verbose_name='Текст')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',)
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'

    def __str__(self):
        return self.text
