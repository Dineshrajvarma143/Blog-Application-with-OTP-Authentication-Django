from django.db import models
from django.contrib.auth.models import User


class Blog(models.Model):
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    author     = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    image      = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']