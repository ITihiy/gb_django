from django.urls import path
from ordersapp import views


app_name = 'ordersapp'


urlpatterns = [
    path('', views.OrderListView.as_view(), name='list'),
    path('create/', views.OrderCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.OrderUpdateView.as_view(), name='update'),
    path('read/<int:pk>/', views.OrderReadView.as_view(), name='read'),
    path('delete/<int:pk>/', views.OrderDeleteView.as_view(), name='delete'),
    path('complete/<int:pk>/', views.complete, name='complete'),
    path('product/<int:pk>/price/', views.get_product_price, name='product_price'),
]
