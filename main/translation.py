from .models import Category, Article, Video, Region, Ad
from modeltranslation.translator import TranslationOptions, register

@register(Category)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'content',)

@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title', 'intro',)

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Ad)
class AdTranslationOptions(TranslationOptions):
    fields = ('title',)