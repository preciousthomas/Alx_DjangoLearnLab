# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # form handling logic here
    return render(request, 'bookshelf/add_book.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # editing logic here
    return render(request, 'bookshelf/edit_book.html', {"book": book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('book_list')

# bookshelf/views.py (safe)
from django.shortcuts import render
from .models import Book
from django import forms
from .forms import ExampleForm

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100, required=False)

def search_books(request):
    form = SearchForm(request.GET)
    books = []
    if form.is_valid():
        q = form.cleaned_data['q']
        books = Book.objects.filter(title__icontains=q)  # ORM prevents SQL injection
    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})

from django.shortcuts import render
from .forms import ExampleForm

def example_form_view(request):
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process data safely
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            return render(request, "bookshelf/form_example.html", {"form": form, "success": True})
    else:
        form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})