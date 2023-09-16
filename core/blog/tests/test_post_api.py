import pytest

from datetime import datetime

from django.urls import reverse

from rest_framework.test import APIClient

from accounts.models.users import User




# Define our attributes before writing ...
# tests to use them in better ways.
@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def common_user():
    user = User.objects.create_user(
        email = "admin@example.com",
        password = "password/test/",
        is_verified = True,
        )
    return user


# this decorator give access to database.
@pytest.mark.django_db      
class TestPostApi:
    client = APIClient()

    def test_get_post_response_200_status(self, api_client):
        """
        test for GET Method on list of posts.
        
        """
        url = reverse("blog:api-v1:post-list")
        response = api_client.get(url)     
        assert response.status_code == 200


    def test_create_post_response_401_status(self, api_client):
        """
        test for 'Failure' POST method on create post by Authorization user.
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title" : "test",
            "content" : "description",
            "status" : True,
            "published_date" : datetime.now()
        }
        response = api_client.post(url, data)
        assert response.status_code == 401


    def test_create_post_response_201_status(self, api_client, common_user):
        """
        test for 'Successfully' POST method on create post by Authorization user.
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "title" : "test",
            "content" : "description",
            "status" : True,
            "published_date" : datetime.now()
        }
        user = common_user
        api_client.force_login(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 201



    def test_create_post_invalid_data_400_status(self, api_client, common_user):
        """
        test for 'Invalid' POST method on create post by Authorization user.
        """
        url = reverse("blog:api-v1:post-list")
        data = {
            "content" : "description",
        }
        user = common_user
        api_client.force_authenticate(user=user)
        response = api_client.post(url, data)
        assert response.status_code == 400
