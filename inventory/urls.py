from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/add_product', views.add_product, name='add_product'),
    path('products/add_category/', views.add_category, name='add_category'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('products/<int:pk>/restock/', views.restock_product, name='restock_product'),
    path('categories/view/', views.view_categories, name='view_categories'),
    path('category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('category/<int:pk>/delete/', views.delete_category, name='delete_category')
]
