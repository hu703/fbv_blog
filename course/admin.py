from django.contrib import admin

# Register your models here.
from course.models import Category,Article,UserDetail
from markdownx.admin import MarkdownxModelAdmin

class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'author',
        'visited',
        'created_at',
        'updated_at'
    ]

admin.site.register(Category)
admin.site.register(UserDetail)
admin.site.register(Article,MarkdownxModelAdmin)