from django.urls import path

from adminapp import views as adminapp

app_name = 'adminapp'


urlpatterns = [
    path('users/', adminapp.UsersListView.as_view(), name='users'),
    path('users/create/', adminapp.UserCreateView.as_view(), name='user_create'),
    path('users/update/<int:pk>/', adminapp.UserEditView.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', adminapp.UserDeleteView.as_view(), name='user_delete'),

    path('categories/', adminapp.ProductCategoryListView.as_view(), name='categories'),
    path('categories/create/', adminapp.ProductCategoryCreateView.as_view(), name='category_create'),
    path('categories/update/<int:pk>/', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', adminapp.ProductCategoryDelete.as_view(), name='category_delete'),

    path('products/<int:pk>/', adminapp.ProductListView.as_view(), name='products'),
    path('products/create/', adminapp.ProductCreateView.as_view(), name='product_create'),
    path('products/update/<int:pk>/', adminapp.ProductEditView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', adminapp.ProductDeleteView.as_view(), name='product_delete'),
    path('product/read/<int:pk>/', adminapp.ProductDetailView.as_view(), name='product_read'),

    path('orders/', adminapp.OrdersListView.as_view(), name='orders'),
    path('orders/update/<int:pk>/', adminapp.OrderStatusUpdateView.as_view(), name='orders_update'),
]
