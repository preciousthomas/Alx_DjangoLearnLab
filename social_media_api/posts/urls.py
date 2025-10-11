from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
path('api/', include('posts.urls')),
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts app routes (if you already have these)
    path('api/accounts/', include('accounts.urls')),

    # ✅ Add this line for the posts app
    path('api/', include('posts.urls')),
]
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts routes (you already have this)
    path('api/accounts/', include('accounts.urls')),

    # ✅ Add this line for posts
    path('api/', include('posts.urls')),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FeedView

urlpatterns = [
    path('feed/', FeedView.as_view(), name='user-feed'),
]
from django.urls import path
from .views import FeedView

urlpatterns = [
    path('feed/', FeedView.as_view(), name='feed'),
]