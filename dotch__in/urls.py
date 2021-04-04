"""dotch__in URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .settings import base
from django.conf.urls.static import static
from shop.views import homepage


urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls', namespace='orders')),
    path('clothing/unisex/', include('shop.urls',namespace='shop')),
    path('creative-gifts/', include('gifting.urls', namespace='gifting')),
    path('', homepage, name='homepage'),
    path('cart/', include('cart.urls', namespace='cart')),
    path('stitching/', include('stitching.urls', namespace='stitching'))


]
if base.DEBUG:
   urlpatterns += static(base.MEDIA_URL,
                         document_root=base.MEDIA_ROOT)