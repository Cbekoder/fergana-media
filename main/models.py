from django.db import models
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    image = models.ImageField(upload_to='images/', verbose_name=_('Image'))
    intro = models.TextField(verbose_name=_('Intro'))
    content = models.TextField(verbose_name=_('Content'))
    views = models.IntegerField(default=0, verbose_name=_('Views'))

    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.title


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    intro = models.TextField(verbose_name=_('Intro'))
    cover = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('Cover Image'))
    url = models.URLField(verbose_name=_('URL'))

    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.title
