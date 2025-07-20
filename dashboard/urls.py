from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_home, name='manager_dashboard'),
    path('orders/', views.all_orders, name='all_orders')
]