from django import forms
from .models import *

class PostForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'PostAutor',
            'Choise',
            'header',
            '_postcategory',
            'text',
            ]
    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        if text is not None and len(text) < 20:
            raise ValidationError({
                "description": "Текст поста не может быть менее 20 символов."
            })

        return cleaned_data

