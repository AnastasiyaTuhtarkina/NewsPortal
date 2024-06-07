from django import forms
from .models import Post, Author
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):

    class Meta:
       model = Post
       fields = [
           'name_post',
           'categories_post',
           'text_post',
       ]
       widgets = {
           'name_post': forms.Textarea(attrs={'class': 'form-taxt', 'cols': 70, 'rows': 3}),
           'text_post': forms.Textarea(attrs={'class': 'form-taxt', 'cols': 70, 'rows': 10}),
       }

    def clean_name(self):
        name = self.cleaned_data["name_post"]
        if name[0].islower():
            raise ValidationError(
                "Название должно начинаться с заглавной буквы"
            )
        return name
    
    def clean_text(self):
        name = self.cleaned_data["text_post"]
        if name[0].islower():
            raise ValidationError(
                "Текст должен начинаться с заглавной буквы"
            )
        return name