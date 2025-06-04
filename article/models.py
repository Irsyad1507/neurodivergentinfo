from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField('Title', max_length=255)
    content = models.TextField('Content')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' - ' + self.author.username