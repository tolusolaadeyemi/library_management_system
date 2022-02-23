from django import forms
from .models import Book


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["book_isbn","book_title","book_author","book_image","book_desc","book_genre_id","book_available_copies","book_total_copies"]
