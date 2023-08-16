from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

# Create your models here.

# getting user model objects
# User = get_user_model()

class Post(models.Model):
    '''
    this is a class to define posts for blog app
    '''
    author = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    status = models.BooleanField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title
    
    def get_snippet(self):
        return self.content[:5]
    
    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})
    

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name