from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view to show library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
# Removed duplicate import statements; already imported at the top.
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("list_books")  # or any existing page
    else:
        form = AuthenticationForm()
    return render(request, "relationship_app/login.html", {"form": form})


def user_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_books")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def user_logout(request):
    logout(request)
    return render(request, "relationship_app/logout.html")