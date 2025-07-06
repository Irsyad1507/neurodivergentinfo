"""
URL configuration for article app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_articles, name='all_articles'),
    path('new/', views.AddArticleView.as_view(), name='new_article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('update/<int:article_id>/', views.update_article, name='update_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('search/', views.search_article, name='search_article'),
    path('text-download/', views.article_text, name='article_text'),
    path('pdf-download/', views.article_pdf, name='article_pdf'),
    path('category/new/', views.AddCategoryView.as_view(), name='new_category'),
    path('category/<str:name>/', views.article_by_category, name='category'),
]
