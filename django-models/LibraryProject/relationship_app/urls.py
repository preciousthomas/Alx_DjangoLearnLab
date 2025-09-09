from django.urls import path
from .views import list_books, LibraryDetailView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("books/", list_books, name="list_books"),  
    path("library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
]

from .views import user_login, user_logout, user_register

urlpatterns += [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("register/", user_register, name="register"),
]