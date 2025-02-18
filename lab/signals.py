from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .utils import send_email_notification

@receiver(post_save, sender=Order)
def send_order_email(sender, instance, created, **kwargs):
    """Send email when order status changes."""
    
    admin_email = "2k23aids06@kiot.ac.in"  # Change to actual admin email
    customer_email = instance.user.email
    order_id = instance.id
    product_name = instance.product.name

    if created:
        # Order Placed: Notify the admin
        subject = f"New Order #{order_id} Placed"
        message = f"A new order has been placed by {instance.user.username}.\nOrder ID: {order_id}\nTotal: ${instance.total_amount}"
        send_email_notification(subject, message, admin_email)

    elif instance.order_status == "PROCESSING":
        # Order Confirmed: Notify the customer
        subject = f"Your Order #{order_id} is Confirmed"
        message = f"Hello {instance.user.username},\nYour order for {product_name} has been confirmed."
        send_email_notification(subject, message, customer_email)

    elif instance.order_status == "COMPLETED":
        # Order Ready: Notify the customer
        subject = f"Your Order #{order_id} is Ready for Pickup"
        message = f"Hello {instance.user.username},\nYour order for {product_name} is now ready for pickup."
        send_email_notification(subject, message, customer_email)

# settings.py
LOGIN_URL = '/login/'
