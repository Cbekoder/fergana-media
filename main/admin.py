from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User, Group
from django.db.models import Model
from modeltranslation.admin import TranslationAdmin
from .models import Category, Article, Video, Region, Ad, Staff

admin.site.unregister([User, Group])

class CustomTranslationAdmin(TranslationAdmin):
    def get_queryset(self, request):
        from django.utils import translation
        translation.activate('uz_Latn')
        return super().get_queryset(request)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        from django.utils import translation
        translation.activate('uz_Latn')
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(CustomTranslationAdmin):
    list_display = ('title',)
    list_display_links = ('title',)

    search_fields = ('title',)
    ordering = ('title',)


@admin.register(Region)
class RegionAdmin(CustomTranslationAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)

@admin.register(Article)
class ArticleAdmin(CustomTranslationAdmin):
    list_display = ('title', 'intro', 'views', 'publish', 'created_at')
    list_display_links = ('title',)

    search_fields = ('title',)
    list_filter = ('publish',)
    date_hierarchy = 'created_at'
    ordering = ('title', 'views', 'created_at')

    # class Media:
    #     js = (
    #         'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    #         'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
    #         'modeltranslation/js/tabbed_translation_fields.js',
    #     )
    #     css = {
    #         'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
    #     }

@admin.register(Video)
class VideoAdmin(CustomTranslationAdmin):
    list_display = ('title', 'intro', 'created_at')
    list_display_links = ('title',)
    list_filter = ('categories__title',)

    search_fields = ('title', 'categories__title')
    ordering = ('title', 'created_at')


@admin.register(Ad)
class AdAdmin(CustomTranslationAdmin):
    list_display = ('title', )
    list_display_links = ('title',)
    search_fields = ('title',)
    ordering = ('title',)


# admin.site.register(Category, CategoryAdmin)

@admin.register(Staff)
class StaffAdmin(TranslationAdmin):
    list_display = ('first_name', 'last_name', 'position', 'licence_no')
    search_fields = ('first_name', 'last_name', 'position', 'licence_no')
    list_filter = ('position',)
