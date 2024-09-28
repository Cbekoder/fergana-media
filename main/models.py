from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Nom'))

    class Meta:
        verbose_name = _('Kategoriya')
        verbose_name_plural = _('Kategoriyalar')

    def __str__(self):
        return self.title


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Nom'))

    class Meta:
        verbose_name = _('Joy')
        verbose_name_plural = _('Joylar')

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Sarlavha'))
    image = models.ImageField(upload_to='images/', verbose_name=_('Rasm'))
    intro = models.TextField(verbose_name=_('Kirish matni'))
    content = models.TextField(verbose_name=_('Batafsil'))
    views = models.IntegerField(default=0, verbose_name=_("Ko'rish soni"))
    publish = models.BooleanField(default=True, verbose_name=_('Chop etish'))
    news_of_the_day = models.BooleanField(default=False, verbose_name=_('Kun yangiligi'))

    categories = models.ManyToManyField(Category, verbose_name=_('Kategoriyalar'))
    region = models.ForeignKey(Region, verbose_name=_('Joy'), on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan sana"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Maqola')
        verbose_name_plural = _('Maqolalar')

    def save(self, *args, **kwargs):
        if self.news_of_the_day:
            Article.objects.filter(news_of_the_day=True).update(news_of_the_day=False)
        super(Article, self).save(*args, **kwargs)


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Sarlavha'))
    intro = models.TextField(verbose_name=_('Kirish matni'))
    cover = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('Rasm'))
    url = models.URLField(verbose_name=_('Link'))

    categories = models.ManyToManyField(Category, verbose_name=_('Kategoriyalar'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan sana"))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videolar')

    def __str__(self):
        return self.title


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Sarlavha'))
    url = models.URLField(verbose_name=_('Link'))
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('Rasm'))

    class Meta:
        verbose_name = _('Reklama')
        verbose_name_plural = _('Reklamalar')

    def __str__(self):
        return self.title
