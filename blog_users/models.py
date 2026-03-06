from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Bloguser(models.Model):
    user =  models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
class Create_blog(models.Model):
    user = models.ForeignKey(Bloguser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    penname = models.CharField(max_length=75,default='null')

    def __str__(self):
        return self.title