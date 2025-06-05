from django.shortcuts import render
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponseRedirect

def all_articles(request):
    articles = Article.objects.all()
    return render(request, 'article/all_articles.html', {
        'articles': articles
    })

def new_article(request):
    submitted = False
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/article/new?submitted=True')
    else:
        form = ArticleForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'article/new_article.html', {
        'form': form, 
        'submitted': submitted
    })
