from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

# getting user model objects
User = get_user_model()

class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name