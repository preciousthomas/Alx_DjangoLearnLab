# bookshelf/forms.py
from django import forms

class ExampleForm(forms.Form):
    """
    Example form to demonstrate CSRF protection and safe form handling.
    """
    name = forms.CharField(max_length=100, required=True, label="Your Name")
    message = forms.CharField(widget=forms.Textarea, required=True, label="Message")