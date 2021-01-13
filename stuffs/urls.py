from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="Homepage"),

    path('user_profile/', views.user_profile, name="user_staff_profile"),
    path('user_profile/update/', views.update_profile, name="update_staff_profile"),
    
    path('Restaurant_profile/', views.res_profile, name="res_profile"),
    path('Restaurant_profile/update/', views.update_res_profile, name="update_res_profile"),

    path('reviews/', views.reviews, name="reviews"),

    path('myitems/', views.allItems, name="myitems"),
    path('add_item/', views.add_item, name="add_item"),
    path('edit_item/<int:id>', views.edit_item, name="edit_item"),
    path('delete_item/<int:id>', views.delete_item, name="delete_item"),
    path('item_details/<int:id>', views.item_details, name="item_view"),

    path('orders/', views.cus_orders, name="cus_orders"),
    path('orders/all/', views.all_orders, name="cus_orders_all"),
    path('orders/today/', views.today_orders, name="cus_orders_today"),
    path('orders/this_month/', views.this_month_orders, name="cus_orders_month"),
    path('orders/this_year/', views.this_year_orders, name="cus_orders_year"),

    path('orders/new/', views.new_orders, name="cus_orders_new"),
    path('orders/started/', views.started_orders, name="cus_orders_started"),
    path('orders/abandoned/', views.abandoned_orders, name="cus_orders_abandoned"),
    path('orders/finished/', views.finished_orders, name="cus_orders_finished"),

    path('orders/view/<int:id>', views.view_orders, name="view_orders"),
    path('orders/accept/<int:id>', views.accept_orders, name="acc_orders"),
    path('orders/reject/<int:id>', views.reject_orders, name="rej_orders"),
    path('orders/finish/<int:id>', views.finish_orders, name="fin_orders"),
    path('orders/delete/<int:id>', views.delete_orders, name="del_orders"),

    path('contact_us/', views.contact_us, name="contact_us_staffview"),
]
