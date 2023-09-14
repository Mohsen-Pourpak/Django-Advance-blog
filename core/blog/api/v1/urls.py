from . import views

from rest_framework.routers import DefaultRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("post", views.PostModelViewSet, basename="post")
router.register("category", views.CategoryModletViewSet, basename="category")
urlpatterns = router.urls


"""
urlpatterns = [
    # path('post/', views.PostList, name="post-list"),
    # path('post/', views.PostList.as_view(), name="post-list"),
    # path('post/<int:pk>/', views.PostDetail, name="post-detail"),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='post-detail')
    # path('post/', views.PostViewSet.as_view({'get':'list'}), name='post-list'),
    # path('post/<int:pk>/', views.PostViewSet.as_view({'get':'retrieve'}), name='post-detail')
    ]
"""
