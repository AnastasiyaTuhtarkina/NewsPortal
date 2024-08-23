from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

class CategoryTranslationSdmin(TranslationAdmin):
    model = Category

class PostTranslationSdmin(TranslationAdmin):
    model = Post

admin.site.register(Author)
admin.site.register(Post, PostTranslationSdmin)
admin.site.register(Category, CategoryTranslationSdmin)
admin.site.register(Comment)
