from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", "ADMIN")
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ("STUDENT", "Student"),
        ("FACULTY", "Faculty"),
        ("ADMIN", "Admin"),
    ]

    email = models.EmailField(unique=True, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    status = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "user_type"]

    objects = CustomUserManager()

    class Meta:
        db_table = 'lab_customuser'
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'

    def __str__(self):
        return self.username


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('TSHIRT', 'T-Shirt'),
        ('CUP', 'Cup'),
        ('3DPRINT', '3D Printing'),
        ('WOODCARVE', 'Wood Carving'),
        ('STICKER', 'Sticker')
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    customization_text = models.CharField(max_length=200, blank=True, null=True)
    customization_font = models.CharField(max_length=50, blank=True, null=True)
    customization_image = models.ImageField(upload_to='customizations/', blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, default='PENDING')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"

from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class LabBooking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]

    id = models.BigAutoField(primary_key=True)
    event_name = models.CharField(max_length=200)
    event_coordinator = models.CharField(max_length=100, null=True, blank=True)
    chief_guest = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=50)
    start_date = models.DateTimeField()  # Changed from from_datetime
    end_date = models.DateTimeField()    # Changed from to_datetime
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    faculty_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='faculty_id_id')
    chief_guest_designation = models.CharField(max_length=100, null=True, blank=True)
    event_description = models.TextField(null=True, blank=True)
    lab = models.CharField(max_length=255)  # Added to match the schema

    def __str__(self):
        return f"{self.event_name} ({self.status})"
    
from django.db.models.signals import post_save
from django.dispatch import receiver
import lab.signals  # Import signals


