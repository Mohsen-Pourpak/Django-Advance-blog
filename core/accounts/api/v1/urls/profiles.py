# from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path
from .. import views


urlpatterns = [
    # User's Profiles
    path("", views.ProfileApiView.as_view(), name="profile"),
]
