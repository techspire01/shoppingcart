from django.urls import path
from . import views

urlpatterns = [
    # Products
    path('', views.product_list, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    # Cart
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<int:item_id>/', views.update_cart_quantity, name='update_quantity'),

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    # Reviews
    path('review/add/<int:product_id>/', views.add_review, name='add_review'),

    # Address
    path('address/', views.address_list, name='address_list'),
    path('address/add/', views.add_address, name='add_address'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('orders/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]

