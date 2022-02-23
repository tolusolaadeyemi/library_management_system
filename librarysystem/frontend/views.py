from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from manager.models import Book
from librarysystem.filters import BookFilter


def index(request):
    all_books = Book.objects.all()
    myFilter = BookFilter(request.GET,queryset=all_books)
    all_books = myFilter.qs
    context = {
        'all_classics': all_books.filter(book_genre_id=2),
        'all_action':all_books.filter(book_genre_id=1),
        'all_mystery':all_books.filter(book_genre_id=3),
        'all_fantasy':all_books.filter(book_genre_id=4),
        'all_history':all_books.filter(book_genre_id=5),
        'all_horror':all_books.filter(book_genre_id=6),
        'all_romance':all_books.filter(book_genre_id=7),
        'all_scifi':all_books.filter(book_genre_id=8),
        'all_bios':all_books.filter(book_genre_id=9),
        'all_cookbooks':all_books.filter(book_genre_id=10),
        'all_selfhelp':all_books.filter(book_genre_id=11),
        'all_crime':all_books.filter(book_genre_id=12),
        'myFilter':myFilter,
    }
    return render(request, 'frontend/index.html',context=context)
