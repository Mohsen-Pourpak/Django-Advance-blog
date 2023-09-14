from datetime import datetime

from django.test import TestCase

from blog.models import Post, Category
from accounts.models import User, Profile

from django.contrib.auth import get_user_model

class TestPostModel(TestCase):

    """ 
    This method is for making our instance more clearly.
    """
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="test FirstName",
            last_name="test LastName",
            description="test Description",
        )

    def test_create_post_with_valid_data(self):
        post = Post.objects.create(
            author = self.profile,
            title = "test",
            content = "description",
            status = True,
            category = None,
            published_date = datetime.now(), 
        )
        self.assertTrue(Post.objects.filter(pk=post.id).exists())
        self.assertEquals(post.title, "test")