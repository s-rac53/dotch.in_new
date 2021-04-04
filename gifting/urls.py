from django.urls import path
from gifting import views


app_name = 'gifting'


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]