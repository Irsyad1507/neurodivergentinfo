from django.shortcuts import render
from .models import Article

def all_articles(request):
    articles = Article.objects.all()
    return render(request, 'article/all_articles.html', {
        'articles': articles
    })
