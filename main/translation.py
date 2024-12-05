from .models import Category, Article, Video, Region, Ad, Staff, Credentials
from modeltranslation.translator import TranslationOptions, register

@register(Category)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'content',)

@register(Video)
class VideoTranslationOptions(TranslationOptions):
    fields = ('title', 'intro', 'content')

@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Ad)
class AdTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Staff)
class StaffTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'position')

@register(Credentials)
class CredentialsTranslationOptions(TranslationOptions):
    fields = ('test_mode_info', 'address')