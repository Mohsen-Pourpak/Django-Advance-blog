# from rest_framework.authtoken.views import ObtainAuthToken
from django.urls import path
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # registrations With Token
    path(
        "registration/",
        views.RegistrationApiView.as_view(),
        name="registration",
    ),
    path(
        "token/login/",
        views.CustomObtainAuthToken.as_view(),
        name="token-login",
    ),
    path(
        "token/logout/",
        views.CustomDiscardAuthToken.as_view(),
        name="token-logout",
    ),
    path("test-email/", views.TestEmailSend.as_view(), name="test-email"),
    # activation
    path(
        "activation/confirm/<str:token>",
        views.ActivationAPIView.as_view(),
        name="activation",
    ),
    # resend activation
    path(
        "activation/resend/",
        views.ActivationResendAPIView.as_view(),
        name="activation-resend",
    ),
    # change pass
    path(
        "change-password/",
        views.ChangePasswordApiView.as_view(),
        name="change-password",
    ),
    # Create JWT in 2 ways:
    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),    # way 1
    path(
        "jwt/create/",
        views.CustomTokenObtainPairView.as_view(),
        name="jwt-create",
    ),  # way 2
    # Refresh token
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    # Verifying Token
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
]
