from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import CustomUser, Product, Order, Payment, LabBooking

from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'user_type', 'department', 'mobile_number', 'status')
    list_filter = ('user_type', 'department', 'status')
    search_fields = ('username', 'first_name', 'last_name', 'mobile_number')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'department', 'mobile_number')}),
        ('Permissions', {'fields': ('user_type', 'status', 'is_active', 'is_staff', 'is_superuser')}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discounted_price', 'stock', 'display_image')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No image"
    display_image.short_description = 'Image'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'total_amount', 'order_status', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('user__email', 'product__name')
    readonly_fields = ('created_at', 'updated_at')
    
    def view_payment(self, obj):
        if hasattr(obj, 'payment'):
            url = reverse('admin:lab_payment_change', args=[obj.payment.id])
            return format_html('<a href="{}">View Payment</a>', url)
        return "No payment"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'amount', 'status', 'razorpay_order_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order__user__email', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('created_at',)


@admin.register(LabBooking)
class LabBookingAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'faculty_id', 'status', 'lab', 'start_date', 'end_date')
    list_filter = ('status', 'department', 'lab')  # Replaced 'venue_type' with 'lab'
    search_fields = ('event_name', 'chief_guest', 'faculty_id__username')



