from django.shortcuts import render

def all_articles(request):
    return render(request, 'article/all_articles.html')
