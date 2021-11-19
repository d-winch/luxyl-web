from django.urls import path
from . import views

#app_name = "etsy_orders"

urlpatterns = [
    path('', views.index, name='etsy_orders'),
    path('<int:order_id>/', views.order, name='order'),
    path('get_orders/', views.get_orders, name='get_orders'),
]