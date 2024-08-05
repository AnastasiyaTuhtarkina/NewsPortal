from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin

class CategoryTranslationSdmin(TranslationAdmin):
    model = Category

class PostTranslationSdmin(TranslationAdmin):
    model = Post

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
