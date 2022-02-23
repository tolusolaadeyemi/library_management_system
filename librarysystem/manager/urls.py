from django.urls import path
from manager import views 

app_name = 'manager'

urlpatterns = [
   path('dashboard/',views.index, name='index'),
   path('user_list/',views.user_list, name='user_list'),
   path('add_user/',views.add_user, name='add_user'),
   path('add_book/',views.add_book,name='add_book'),
   path('update_book/<str:pk>/',views.update_book,name='update_book'),
   path('update_user/<str:pk>/',views.update_user,name='update_user'),
   path('delete_book/<str:pk>/',views.delete_book,name='delete_book'),
   path('delete_user/<str:pk>/',views.delete_user,name='delete_user'),
   path('book_requests/',views.book_requests,name='book_requests'),
   path('approve_book_request/<int:pk>/',views.approve_book_request,name='approve_book_request'),
   path('return_book/<int:pk>/',views.return_book,name='return_book'),
   path('loan_list/',views.loan_list,name='loan_list'),
]