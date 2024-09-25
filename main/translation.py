from .models import Category, Article, Video
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