from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Article(models.Model):
    title = models.CharField('Title', max_length=255)
    content = models.TextField('Content')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' - ' + self.author.username
    
    def get_absolute_url(self):
        return reverse('all_articles')