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
# blog/urls.py (append only)

from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

app_name = "blog"

urlpatterns += [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
# blog/urls.py (append)

from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns += [
    path('posts/<int:post_pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment_update'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
]
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Comment

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']  # adjust fields as needed

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = '/'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    from django.urls import path
from . import views

urlpatterns = [
    # --- Post URLs ---
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # --- Comment URLs ---
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]
# Append to blog/urls.py

from .views import TagListView, PostsByTagView, ManagePostTagsView, PostSearchView

urlpatterns += [
    # tags
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:tag_slug>/', PostsByTagView.as_view(), name='posts-by-tag'),

    # manage tags per post (author only)
    path('post/<int:pk>/tags/manage/', ManagePostTagsView.as_view(), name='manage-post-tags'),

    # search
    path('search/', PostSearchView.as_view(), name='post-search'),
]
path('search/', views.search_posts, name='search_posts'),
from .views import PostByTagListView

urlpatterns = [
    # ... existing urls
    path('tags/<str:tag_name>/', PostByTagListView.as_view(), name='posts_by_tag'),
]