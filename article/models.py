from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Article(models.Model):
    title = models.CharField('Title', max_length=255)
    content = models.TextField('Content')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField('Category', max_length=255, default='Uncategorised')
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' - ' + self.author.username
    
    def get_absolute_url(self):
        return reverse('all_articles')
    
class Category(models.Model):
    name = models.CharField('Category Name', max_length=255)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('all_articles')