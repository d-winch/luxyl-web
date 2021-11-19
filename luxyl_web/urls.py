from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('etsy_orders/', include('etsy_orders.urls')),
]