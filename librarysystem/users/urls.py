from django.urls import path
from users import views 

app_name = 'users'

urlpatterns = [
    path('homepage/',views.homepage, name='homepage'),
    path('book/<str:pk>/', views.book_detail, name='book_detail'),
    path('borrow_book/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('pending_requests/', views.pending_requests, name='pending_requests'),
    path('overdue_books', views.overdue_books, name='overdue_books'),
    path('pay_fees/<int:pk>/', views.pay_fees, name='pay_fees'),
    path('payment_confirmation/', views.payment_confirmation, name='payment_confirmation'),
]