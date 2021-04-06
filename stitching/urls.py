from django.urls import path
from stitching import views

app_name = 'stitching'

urlpatterns = [

    path('', views.stitching_view, name='stitching_view'),


]