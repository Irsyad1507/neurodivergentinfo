from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages


def all_articles(request):
    articles = Article.objects.all()
    return render(request, 'article/all_articles.html', {
        'articles': articles
    })

def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    return render(request, 'article/article_detail.html', {
        'article': article
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


def update_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    submitted = False
    
    if request.method == 'POST':
        # Handle traditional form submission
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f'/article/update/{article_id}?submitted=True')
    elif request.method == 'PUT':
        # Handle PUT request (AJAX)
        try:
            data = json.loads(request.body)
            form = ArticleForm(data, instance=article)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Article updated successfully'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    else:
        form = ArticleForm(instance=article)
        if 'submitted' in request.GET:
            submitted = True
    
    return render(request, 'article/update_article.html', {
        'form': form,
        'submitted': submitted,
        'article': article
    })


@csrf_exempt
def update_article_api(request, article_id):
    """API endpoint specifically for PUT requests"""
    if request.method == 'PUT':
        article = get_object_or_404(Article, pk=article_id)
        try:
            data = json.loads(request.body)
            form = ArticleForm(data, instance=article)
            if form.is_valid():
                form.save()
                return JsonResponse({'success': True, 'message': 'Article updated successfully'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def delete_article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    
    if request.method == 'DELETE':
        # Handle AJAX DELETE request
        article.delete()
        return JsonResponse({'success': True, 'message': 'Article deleted successfully'})
    elif request.method == 'POST':
        # Handle traditional form POST request (fallback)
        article.delete()
        messages.success(request, ("Article Deleted"))
        return redirect('all_articles')
    else:
        # Handle GET request (current implementation for backward compatibility)
        article.delete()
        messages.success(request, ("Article Deleted"))
        return redirect('all_articles')