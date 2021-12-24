from authapp import views as authapp
from django.urls import path

app_name = 'authapp'


urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('edit/', authapp.edit, name='edit'),
    path('register/', authapp.register, name='register'),
    path('verify/<email>/<activation_key>/', authapp.verify, name='verify'),
]
