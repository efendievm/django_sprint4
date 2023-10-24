from datetime import datetime

from django.db import models
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import BaseModel

User = get_user_model()


class Location(BaseModel):
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Category(BaseModel):
    title = models.CharField('Заголовок', max_length=256)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; разрешены символы '
                   'латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title


class PostQueryset(models.QuerySet):
    def enriched_posts(self):
        return self.select_related(
            'location',
            'author',
            'category')

    def authors_posts(self):
        return self.enriched_posts().annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def visible_posts(self):
        return self.authors_posts().filter(
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True)


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQueryset(self.model)

    def enriched_posts(self):
        return self.get_queryset().enriched_posts()

    def authors_posts(self):
        return self.get_queryset().authors_posts()

    def visible_posts(self):
        return self.get_queryset().visible_posts()


class Post(BaseModel):
    title = models.CharField('Заголовок', max_length=256)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)
    objects = models.Manager()
    posts = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title


class CommentWithAuthorQueryset(models.QuerySet):
    def comments(self):
        return self.select_related(
            'author'
        ).order_by('created_at')


class CommentWithAuthorManager(models.Manager):
    def get_queryset(self):
        return CommentWithAuthorQueryset(self.model).comments()


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Публикация')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    with_author = CommentWithAuthorManager()

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.post_id})

    def __str__(self):
        return self.text
