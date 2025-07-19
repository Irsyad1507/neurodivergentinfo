from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, CreateView
from .models import Article, Category
from .forms import ArticleForm
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.views.decorators.http import require_POST
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


def all_articles(request):
    article_list = Article.objects.all()

    paginator = Paginator(article_list.order_by('-date_created'), 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    iterator = "o" * articles.paginator.num_pages

    return render(request, 'article/all_articles.html', {
        'article_list': article_list, 
        'articles': articles, 
        'iterator': iterator,
    })

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'article/article_detail.html'

class AddArticleView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article/new_article.html'

class AddCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'article/new_category.html'
    fields = '__all__'

@login_required
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
    
@require_POST
def search_article(request):
    searched = request.POST.get('searched')
    articles = Article.objects.filter(title__contains=searched)
    return render(request, 'article/search_article.html', 
                  {'searched': searched, 
                   'articles': articles})

@login_required
def article_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=articles.txt'
    # Designate the model
    articles = Article.objects.all()

    # List comprehension of article details
    lines = [f"{article.title}\nBy: {article.author} | {article.date_created}\n{article.content}\n\n\n" for article in articles]

    # Write to text file
    response.writelines(lines)
    return response

@login_required
def article_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    # Designate The Model
    articles = Article.objects.select_related('author').all()

    lines = [
        item for article in articles 
        for item in [article.title, article.author.username, str(article.date_created), article.content, ""]
    ]

    # for article in articles:
    #     lines.append(str(article.title))
    #     lines.append(str(article.author))
    #     lines.append(str(article.date_created))
    #     lines.append(str(article.content))
    #     lines.append(" ")

    for line in lines:
        textob.textLine(line)

    # Finish up
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    # Return something
    return FileResponse(buf, as_attachment=True, filename='articles.pdf')

def article_by_category(request, name):
    article_by_category = Article.objects.filter(category=name.replace('-', ' '))
    return render(request, 'article/category.html', {
        'name': name.replace('-', ' '), 
        'article_by_category': article_by_category})