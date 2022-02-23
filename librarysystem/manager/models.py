from django.db import models
from accounts.models import User

class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True,auto_created=True)
    genre_name = models.CharField(max_length=50)

    
    def __str__(self):
        return self.genre_name


class Book(models.Model):
    book_isbn = models.IntegerField(primary_key=True,auto_created=True)
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=1000)
    book_image = models.CharField(max_length=550)
    book_desc = models.TextField()
    LOAN_STATUS = (
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    book_availability_status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        null=True,
        default='a',
        help_text='Book availability',
    )

    book_genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)
    book_total_copies = models.IntegerField(default=10)
    book_available_copies = models.IntegerField(default=10)

    def __str__(self):
        return self.book_title

    # def display_genre(self):
    #     """Create a string for the Genre. This is required to display genre in Admin."""
    #     return ', '.join(Genre.genre_name for book_genre_id in self.genre_name.all()[:3])

    # display_genre.short_description = 'Genre'

class BookRequests(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    book_isbn = models.ForeignKey(Book, on_delete=models.CASCADE)
    REQUEST_STATUS = (
        ('p', 'Pending'),
        ('a', 'Approved'),
        ('d', 'Denied'),
    )

    request_approval_status = models.CharField(
        max_length=1,
        choices=REQUEST_STATUS,
        blank=True,
        default='p',
        help_text='Book Request',
    )
    request_date = models.DateTimeField(auto_now_add=True)