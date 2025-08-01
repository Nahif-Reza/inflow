from django.urls import path
from . import views


urlpatterns = [
    path('', views.storefront_home, name='storefront_home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('account/', views.account_info, name='account_info'),
    path('logout/', views.logout_user, name='logout_user'),
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('account/update_profile/', views.update_profile, name='update_profile'),
    path('account/change_password/', views.change_password, name='change_password'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item')

]