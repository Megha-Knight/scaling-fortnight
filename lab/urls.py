from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static




app_name = 'lab'

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # ✅ Fixed duplicate name issue
    
    # Dashboard URLs
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),  # ✅ Added this
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('accounts/login/', views.login_view, name='accounts_login'),
    
    # Product URLs
    path('products/', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='customize_product'),
    path('product/<int:product_id>/order/', views.create_order, name='create_order'),
    path('shop/', views.product_list, name='shop'),
    path('lab/lab_booking/', views.lab_booking, name='lab_booking'),
    path('lab/bookings/', views.lab_booking_list, name='lab_booking_list'),
    path('lab-bookings/', views.lab_booking_list, name='lab_booking_list'),


    
    # Payment URLs
    path('api/payment/initiate/<int:order_id>/', views.initiate_payment, name='initiate_payment'),
    path('api/payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment/failure/<int:order_id>/', views.payment_failure, name='payment_failure'),

    # Order URLs
    path('orders/history/', views.order_history, name='order_history'),
    
    # Lab Booking URLs
    path('book/', views.book_lab, name='book_lab'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('api/events/', views.get_events, name='get_events'),
    
    # Admin Dashboard URLs
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # User Management
    path('admin_dashboard/users/', views.user_list, name='user_list'),
    path('admin_dashboard/users/add/', views.add_user, name='add_user'),
    path('admin_dashboard/users/<int:pk>/update/', views.update_user, name='update_user'),
    path('admin_dashboard/users/<int:pk>/delete/', views.delete_user, name='delete_user'),
    
    # Product Management
    path('admin_dashboard/products/', views.admin_product_list, name='admin_product_list'),
    path('admin_dashboard/products/add/', views.add_product, name='add_product'),
    path('admin_dashboard/products/<int:pk>/update/', views.update_product, name='update_product'),
    path('admin_dashboard/products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    
    # Order Management
    path('admin_dashboard/orders/', views.admin_orders, name='admin_orders'),
    path('admin_dashboard/orders/update_order_status/', views.update_order_status, name='update_order_status'),
    
    # Lab Booking Management
    path('bookings/', views.admin_lab_bookings, name='admin_lab_bookings'),
    path('admin/bookings/<int:pk>/update-status/', views.update_booking_status, name='update_booking_status'),
    path('api/check-availability/', views.check_availability, name='check_availability'),
    path('api/create-booking/', views.create_booking, name='create_booking'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
