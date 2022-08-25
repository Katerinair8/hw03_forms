from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200, verbose_name='title')
    slug = models.SlugField(unique=True, verbose_name='slug')
    description = models.TextField(verbose_name='description')

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(verbose_name='text')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='date')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.text
