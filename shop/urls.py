from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [

    path('', views.product_list, name='product_list'),
    path('clothing/unisex/<slug:category_slug>/', views.product_list, name='product_list'),
    path('clothing/unisex/<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),





]