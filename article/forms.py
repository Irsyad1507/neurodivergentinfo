from django import forms
from django.forms import ModelForm
from .models import Article, Category

options = Category.objects.all().values_list('name', 'name')
option_list = [option for option in options]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'author', 'category', 'content', 'snippet', 'header_image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'authorBox', 'type': 'hidden'}),
            'category': forms.Select(choices=option_list, attrs={'class': 'form-select'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            'snippet': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Snippet from the content'}),
        }