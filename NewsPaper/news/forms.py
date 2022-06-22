from django.forms import ModelForm
from .models import Post, CategoryUser, Category
from django import forms



class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['post_type', 'post_title', 'post_text', 'post_author', 'post_category']
        widgets = {
            'post_author': forms.HiddenInput(),
        }


class SubForm(ModelForm):
    class Meta:
        model = CategoryUser
        fields = ['user', 'category']
        widgets = {
                'user': forms.HiddenInput(),
        }