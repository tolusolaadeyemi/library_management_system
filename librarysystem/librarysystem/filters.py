import django_filters
from django_filters import CharFilter,ModelChoiceFilter
from manager.models import Book,Genre


class BookFilter(django_filters.FilterSet):
    book_title = CharFilter(field_name='book_title',label='Title',lookup_expr='icontains')
    book_author = CharFilter(field_name='book_author',label='Author',lookup_expr='icontains')
    book_genre_id = ModelChoiceFilter(field_name='book_genre_id',label='Genre',queryset=Genre.objects.all())
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['book_isbn','book_availability_status','book_desc','book_image','book_available_copies','book_total_copies']