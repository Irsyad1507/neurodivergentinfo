from django import forms
from django.forms import ModelForm
from .models import Article, Category

options = Category.objects.all().values_list('name', 'name')
option_list = [option for option in options]

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'category', 'author')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Content'}),
            'author': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Author'}),
            'category': forms.Select(choices=option_list, attrs={'class': 'form-select'}),
        }