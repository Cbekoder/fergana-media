from django.contrib import admin
from .models import Category, Article, Video

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )

    search_fields = ('title', )


admin.site.register(Category, CategoryAdmin)

