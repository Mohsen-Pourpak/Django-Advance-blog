from datetime import datetime

from django.test import TestCase, Client
from django.urls import reverse

from accounts.models.users import User
from accounts.models.profiles import Profile

from blog.models import Post, Category


class TestBlogViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email="test@example.com", password="testpassword")
        self.profile = Profile.objects.create(
            user=self.user,
            first_name="test FirstName",
            last_name="test LastName",
            description="test Description",
        )

        self.post = Post.objects.create(
            author = self.profile,
            title = "test",
            content = "description",
            status = True,
            category = None,
            published_date = datetime.now(), 
        )

    def test_blog_index_url_successful_response(self):
        url = reverse("blog:index")
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(str(response.content).find("index"))
        self.assertTemplateUsed(response, template_name= "index.html")


    def test_blog_post_detail_logged_in_response(self):
        self.client.force_login(self.user)
        url = reverse("blog:post-detail", kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)


    def test_blog_post_detail_anonymous_response(self):
        url = reverse("blog:post-detail", kwargs={'pk':self.post.id})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)