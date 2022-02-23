from django.contrib import admin

from .models import Book,BookRequests,Genre
from accounts.models import User
from users.models import Borrower,Payments

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_title','book_author')
@admin.register(BookRequests)
class BookRequestsAdmin(admin.ModelAdmin):
    list_display = ('user_id','book_isbn','request_approval_status')
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre_id","genre_name")
admin.site.register(Borrower)
admin.site.register(User)
admin.site.register(Payments) 