"""gb_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from mainapp import views as mainapp_views

urlpatterns = [
    path('', mainapp_views.index, name='mainapp_index'),
    path('', include('social_django.urls', namespace='social')),
    path('products/', include('mainapp.urls', namespace='products')),
    path('orders/', include('ordersapp.urls', namespace='ordersapp')),
    path('auth/', include('authapp.urls', namespace='authapp')),
    path('basket/', include('basketapp.urls', namespace='basketapp')),
    path('contact/', mainapp_views.contact, name='mainapp_contact'),
    path('admin/', include('adminapp.urls', namespace='adminapp')),
    # path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
