from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name="blog/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="blog/logout.html"), name='logout'),
    path('profile/', views.profile, name='profile'),  # Profile view will be added in Step 4
]
# blog/urls.py  (append or create)
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # posts CRUD
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/new/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
# django_blog/urls.py  (append if needed)
from django.urls import path, include

urlpatterns += [
    path('', include('blog.urls')),
]