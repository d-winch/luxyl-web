from django.urls import path
from . import views

#app_name = "etsy_orders"

urlpatterns = [
    path('', views.index, name='index'),
    path('verify_shipping/', views.verify_shipping, name='verify_shipping'),
    path('create_order/', views.create_order, name='create_order'),
    path('labels_tracking/', views.labels_tracking, name='labels_tracking'),
    path('submit_tracking/', views.submit_tracking, name='submit_tracking'),
]