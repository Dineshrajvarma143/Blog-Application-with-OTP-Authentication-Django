from django.db import models

# Create your models here.
class Bloguser(models.Model):
    full_name = models.CharField(max_length=200,)
    age = models.IntegerField()
    phone = models.CharField(max_length=11)
    registered_email = models.EmailField(max_length=254)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.full_name
    
class Create_blog(models.Model):
    user = models.ForeignKey(Bloguser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    penname = models.CharField(max_length=75,default='null')


    def __str__(self):
        return self.penname