from django.contrib import admin
from django import forms
from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User, Group
from django.db.models import Model, TextField
from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget
from .models import Category, Article, Video, Region, Ad, Staff, Credentials
from django.utils import translation


admin.site.unregister([Group])

class CustomTranslationAdmin(TranslationAdmin):
    def get_queryset(self, request):
        from django.utils import translation
        translation.activate('uz_Latn')
        return super().get_queryset(request)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        translation.activate('uz_Latn')
        if db_field.name == "content":
            kwargs['widget'] = CKEditorWidget()
        elif db_field.name == "intro":
            kwargs['widget'] = forms.Textarea()
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
    readonly_fields = ['created_at', 'views']


@admin.register(Video)
class VideoAdmin(CustomTranslationAdmin):
    list_display = ('title', 'intro', 'created_at')
    list_display_links = ('title',)
    list_filter = ('categories__title',)

    search_fields = ('title', 'categories__title')
    ordering = ('title', 'created_at')
    readonly_fields = ['created_at']
    formfield_overrides = {
        TextField: {'widget': CKEditorWidget},
    }

# @admin.register(Ad)
# class AdAdmin(CustomTranslationAdmin):
#     list_display = ('title', )
#     list_display_links = ('title',)
#     search_fields = ('title',)
#     ordering = ('title',)


# admin.site.register(Category, CategoryAdmin)

@admin.register(Staff)
class StaffAdmin(TranslationAdmin):
    list_display = ('first_name', 'last_name', 'position', 'licence_no')
    search_fields = ('first_name', 'last_name', 'position', 'licence_no')
    list_filter = ('position',)


@admin.register(Credentials)
class CredentialsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Contact Information', {
            'fields': ('domain', 'phone', 'email', 'address')
        }),
        ('Social Media Links', {
            'fields': ('instagram', 'telegram', 'youtube', 'facebook')
        }),
        ('Test Mode', {
            'fields': ('is_test_mode', 'test_mode_info')
        }),
        ('Telegram Settings', {
            'fields': ('botToken', 'channel_id')
        }),
    )
    def has_add_permission(self, request):
        if Credentials.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        return False