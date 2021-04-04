from django.urls import path
from orders import views


app_name = 'orders'


urlpatterns = [

      path('create/shop/', views.order_create, name='order_create_shop'),
      path('create/gifting/', views.order_create_gifting, name='order_create_gifting'),
      path('create/gifting/<int:id>/<slug:slug>', views.order_create_gifting, name='order_create_gifting'),
      path('create/gifting/<int:id>/<slug:slug>/<str:variant>', views.order_create_gifting, name='order_create_gifting'),
      path('bulkorders/<int:id>/<slug:slug>', views.bulk_orders, name='bulk_orders'),
      path('submit/<int:id>/<slug:slug>', views.order_create_bulk, name='order_create_bulk'),
      path('review/', views.review_form, name='review_form'),
      path('review/<int:star>/', views.review_form, name='review_form'),
      path('create/stitching/', views.order_create_stitching, name='order_create_stitching'),
]