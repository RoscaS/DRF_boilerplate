from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, default="")
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=timezone.now)
    weight = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-weight']

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=300, blank=True, null=True)
    description = models.TextField(max_length=1024, blank=True, default="")
    body = models.TextField(max_length=64000, blank=True, null=True)
    highlighted = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    weight = models.PositiveIntegerField(default=0)
    image = models.ImageField(verbose_name='Image', blank=True, null=True, default="placeholder-image.png")
    slug = models.SlugField(max_length=300, blank=True, null=True, unique=True)
    created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=timezone.now)
    category = models.ForeignKey('Category', related_name='articles', on_delete=models.CASCADE, null=False)
    author = models.ForeignKey('users.User', related_name='articles', on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.title
