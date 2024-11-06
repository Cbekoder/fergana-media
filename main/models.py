from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import sendArticle


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
    to_send_bot = models.BooleanField(default=True, verbose_name=_("Telegram kanalga yuborish"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Maqola')
        verbose_name_plural = _('Maqolalar')

    # def save(self, *args, **kwargs):
    #
    #     super(Article, self).save(*args, **kwargs)


class Video(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Sarlavha'))
    intro = models.TextField(verbose_name=_('Kirish matni'))
    cover = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('Rasm'))
    url = models.URLField(verbose_name=_('Link'))
    to_send_bot = models.BooleanField(default=True, verbose_name=_("Telegram kanalga yuborish"))

    categories = models.ManyToManyField(Category, verbose_name=_('Kategoriyalar'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Qo'shilgan sana"))

    class Meta:
        verbose_name = _('Video')
        verbose_name_plural = _('Videolar')

    def __str__(self):
        return self.title

class BotMessageIDs(models.Model):
    article = models.OneToOneField(Article, on_delete=models.CASCADE, null=True, unique=True, verbose_name=_('Article'))
    video = models.OneToOneField(Video, on_delete=models.CASCADE, null=True, unique=True, verbose_name=_('Article'))
    message_id = models.IntegerField(verbose_name=_("Telegram Message Id"))


class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Sarlavha'))
    url = models.URLField(verbose_name=_('Link'))
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('Rasm'))

    class Meta:
        verbose_name = _('Reklama')
        verbose_name_plural = _('Reklamalar')

    def __str__(self):
        return self.title


class Staff(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('Ism'), null=True, blank=True)
    last_name = models.CharField(max_length=100, verbose_name=_('Familya'), null=True, blank=True)
    photo = models.ImageField(upload_to='staff/', verbose_name=_('Rasm'), blank=True, null=True,)
    position = models.CharField(max_length=100, verbose_name=_('Lavozim'), null=True, blank=True)
    licence_no = models.SmallIntegerField(verbose_name=_('Guvohnoma raqami'), null=True, blank=True)

    class Meta:
        verbose_name = _('Hodim ')
        verbose_name_plural = _('Hodimlar')

    def __str__(self):
        return str(self.id)
