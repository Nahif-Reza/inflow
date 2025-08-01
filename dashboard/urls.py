from django.urls import path
from . import views


urlpatterns = [
    path('', views.manager_home, name='manager_dashboard'),
    path('orders/', views.all_orders, name='all_orders'),
    path('logout/', views.logout_manager, name='logout'),
    path('profit/', views.profit_analysis, name='profit_analysis'),
    path('invoices/', views.invoice_list, name='invoice_list'),
    path('tax-delivery/', views.tax_delivery, name='tax_and_delivery_settings'),
    path('customer-list/', views.customer_list, name='customer_list'),
    path('transactions/', views.all_transactions, name='all_transactions'),
    path('forecast/', views.forecast, name='forecast')
]