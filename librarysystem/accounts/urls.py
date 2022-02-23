from django.urls import path
from accounts import views 

app_name = 'accounts'

urlpatterns = [
    path('signup/',views.signup, name='signup'),
    path('login/',views.user_login, name='login'),
    path('logout', views.user_logout, name= 'logout'),
    path('check_user', views.check_user, name= 'check_user'),
]