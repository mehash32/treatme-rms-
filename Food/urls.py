from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),

    path('user_profile/', views.user_profile, name="user_profile"),
    path('update_profile/', views.update_profile, name="update_profile"),
    
    path('menus/', views.res_menu, name="menu"),
    path('item-details/<int:id>', views.item_details, name="item_details"),
    path('restaurant/', views.res_list.as_view(), name="restaurant"),
    path('restaurant_menu/<int:id>', views.res_menu, name="restaurant_menu"),

    path('rate/<int:id>', views.rate_item, name="rate-item"),
    path('comment/<int:id>', views.add_comment, name="comment-item"),
    path('comment/delete/<int:id>', views.delete_comment, name="delete-comment-item"),
    path('comment/edit/<int:id>/', views.edit_comment, name="edit-comment-item"),

    path('review/<int:id>', views.review, name="review"),
    path('review/delete/<int:id>', views.delete_review, name="delete_review"),

    path('add_to_wishlist/<int:id>', views.add_to_wishlist, name="add_to_wishlist"),
    path('remove_from_wishlist/<int:id>', views.remove_from_wishlist, name="remove_from_wishlist"),
    path('clear_wishlist', views.clear_wishlist, name="clear_wishlist"),
    path('wishlist/', views.wishlist, name="wishlist"),

    path('orders/', views.order_history, name="order_list"),

    path('cart/', views.order_cart, name="order_cart"),
    path('add_to_cart/<int:id>/', views.add_to_order_cart, name="add_to_order_cart"),
    path('edit_orders/<int:id>/', views.edit_order_cart, name="edit_order_cart"),
    path('remove_from_cart/<int:id>/', views.remove_from_order_cart, name="remove_from_order_cart"),
    path('cart/delete', views.delete_order_cart, name="delete_cart"),
    
    path('cart/apply_voucher', views.apply_voucher, name="apply_voucher"),
    path('cart/remove_voucher', views.remove_voucher, name="remove_voucher"),

    path('checkout/', views.checkout, name="checkout"),
    path('add_user_address/', views.add_user_address, name="user_address"),
    path('confirm/', views.order_confirm, name="order_confirm"),

    path('payment/<int:id>', views.payment, name="payment"),

    path('search_price_range/', views.search_price_range, name="search_price_range"),

    path('contact_us/', views.contact_us, name="contact_us_userview"),
]
