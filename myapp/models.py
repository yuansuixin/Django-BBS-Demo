from django.db import models

# Create your models here.

class Articles(models.Model):
    title = models.CharField(max_length=64)
    create = models.DateTimeField(auto_now_add=True)
    content = models.TextField()








