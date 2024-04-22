from django.contrib import admin

# Register your models here.
from articles.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'text']
    search_fields = ['name', 'text']