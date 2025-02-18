from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from .models import CustomUser, Product, Order, Payment, LabBooking
from .forms import CustomUserCreationForm, ProductForm, OrderForm, LabBookingForm
import razorpay
import json

def is_admin(user):
    return user.user_type == 'ADMIN'

def is_faculty(user):
    return user.user_type == 'FACULTY'

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import CustomUser
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser  # Ensure you import your custom user model

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import CustomUser

from django.contrib.auth import get_user_model
import mysql.connector 
con = mysql.connector.connect(user='root',host= 'localhost',db = 'idealab', passwd = 'arun')
cur = con.cursor()



CustomUser = get_user_model()  # Ensures compatibility with Django's authentication system


def login_view(request,cur = cur):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        
        cur.execute('SELECT user_type FROM lab_customuser WHERE username = %s', (username,))
        data = cur.fetchone()  # Fetch single row
        print(data)

        if data:  # Check if user_type is retrieved
            user_type = data[0]
            print(user_type)  # Extract user_type
            authenticated_user = authenticate(request, username=username, password=password)
            print("auth",authenticated_user)

            if authenticated_user is not None:
                login(request, authenticated_user)

                # Redirect based on user type
                if user_type == 'ADMIN':
                    return redirect('/admin_dashboard') 
                elif user_type == 'FACULTY':
                    return render(request, 'lab/dashboard.html')
                elif user_type == 'USER':
                    print('HI')
                    return redirect('/products')
                else:
                    return redirect('/products')        # Default redirection
            else:
                return render(request, 'lab/login.html', {'error': 'Invalid credentials'})

        return render(request, 'lab/login.html', {'error': 'User not found'})

    # Handle GET request by rendering login page
    return render(request, 'lab/login.html')



@login_required
def logout_view(request):
    logout(request)
    return render(request, 'lab:login.html')



@login_required
@user_passes_test(is_faculty)
def faculty_dashboard(request):
    bookings = LabBooking.objects.filter(faculty=request.user).order_by('created_at')
    context = {
        'bookings': bookings,
        'pending_bookings': bookings.filter(status='PENDING').count(),
        'approved_bookings': bookings.filter(status='APPROVED').count()
    }
    return render(request, 'lab:dashboard.html', context)

@login_required
def product_list(request):
    category = request.GET.get('category')
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    return render(request, 'lab/product_list.html', {'products': products})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderForm(product_category=product.category)
    return render(request, 'lab/customize_product.html', {'product': product, 'form': form})

import json
import time
import razorpay
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Payment
from .forms import OrderForm

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES, product_category=product.category)

        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.product = product
            order.total_amount = product.discounted_price * form.cleaned_data['quantity']

            # Handle file upload
            if 'user_image' in request.FILES:
                order.custom_image = request.FILES['user_image']

            # Handle text customization for T-shirts and Cups
            if product.category in ['TSHIRT', 'CUP']:
                order.custom_text = form.cleaned_data.get('custom_text')
                order.font_style = form.cleaned_data.get('font_style')

            order.save()

            # Create Razorpay Order
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            razorpay_order = client.order.create({
                'amount': int(order.total_amount * 100),
                'currency': 'INR',
                'payment_capture': '1'
            })


            print(f"✅ Razorpay Order Created: {razorpay_order['id']}")

            # Save Payment details
            payment = Payment.objects.create(
                order=order,
                razorpay_order_id=razorpay_order['id'],
                amount=order.total_amount
            )

            return render(request, 'lab/payment.html', {
                'order': order,
                'payment': payment,
                'razorpay_key': settings.RAZORPAY_KEY_ID
            })

    return redirect('lab:payment_callback')

def initiate_payment(request, order_id):
    try:
        print("💰 Initiating Payment")
        order = Order.objects.get(id=order_id)
        
        # Check if Payment exists
        payment = Payment.objects.filter(order=order).first()
        if not payment:
            return JsonResponse({'error': 'No payment record found for this order'}, status=404)

        print(f"✅ Using Existing Razorpay Order ID: {payment.razorpay_order_id}")

        return JsonResponse({
            'message': 'Payment initiated',
            'order_id': order.id,
            'razorpay_order_id': payment.razorpay_order_id,  # Use existing ID
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'razorpay_amount': order.total_amount * 100
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def payment_callback(request):
    print("🔄 Payment Callback Received")
    print("Full Request Method:", request.method)
    print("Request Headers:", request.headers)
    print("Request Body:", request.body)

    try:
        data = json.loads(request.body)
        order_id = data.get('razorpay_order_id', '').strip()
        payment_id = data.get('razorpay_payment_id', '')
        signature = data.get('razorpay_signature', '')

        print(f"🔍 Searching for Payment with Order ID: {order_id}")

        # Add a small delay in case of DB sync issues
        for _ in range(3):  # Retry 3 times
            payment = Payment.objects.filter(razorpay_order_id__iexact=order_id).first()
            if payment:
                break
            time.sleep(1)  # Wait before retrying

        if not payment:
            print(f"❌ No payment found for Razorpay Order ID: {order_id}")
            return JsonResponse({'success': False, 'error': 'Payment not found'}, status=404)

        order = payment.order

        # Verify Payment Signature
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })

        # Update payment and order status
        payment.status = 'SUCCESS'
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.save()

        order.order_status = 'PROCESSING'
        order.save()

        print(f"✅ Payment Successful for Order {order.id}")

        return JsonResponse({'success': True, 'order_id': order.id})

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def payment_success(request, order_id):
    """Handle successful payment"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'payment': order.payment  # Use OneToOneField direct reference
    }
    return render(request, 'lab/payment_success.html', context)

@login_required
def payment_failure(request, order_id):
    """Handle failed payment"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'payment': order.payment
    }
    return render(request, 'lab/payment_failure.html', context)






@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'lab/order_history.html', {'orders': orders})

def send_order_confirmation_email(order = {}):
    context = {
        'order': order,
        'user': order.user,
    }
    subject = f'Order Confirmation - #{order.id}'
    html_message = render_to_string('lab/invoice.html', context)
    plain_message = render_to_string('lab/email/order_confirmation.txt', context)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        html_message=html_message
    )

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from lab.forms import LabBookingForm
from lab.models import LabBooking

@login_required
def book_lab(request):
    if request.method == 'POST':
        print("📌 Received POST request")  # Debugging Step 1
        print("📌 Request POST data:", request.POST)  # Debugging Step 2

        form = LabBookingForm(request.POST)
        if form.is_valid():
            print("✅ Form is valid")  # Debugging Step 3
            print("✅ Cleaned Data:", form.cleaned_data)  # Debugging Step 4

            booking = form.save(commit=False)
            booking.faculty_id = request.user
            booking.department = request.user.department
            booking.status = 'Pending'

            try:
                booking.save()
                print("✅ Booking successfully saved!")  # Debugging Step 5
                messages.success(request, 'Lab booking request submitted successfully!')
                return redirect('calendar_view')

            except Exception as e:
                print("❌ Error while saving booking:", str(e))  # Debugging Step 6

        else:
            print("❌ Form errors:", form.errors)  # Debugging Step 7

    else:
        form = LabBookingForm()

    return render(request, 'lab/lab_booking.html', {'form': form})


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from lab.models import LabBooking
from lab.forms import LabBookingForm

@csrf_exempt  # Remove if using proper CSRF setup
@login_required
def create_booking(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = LabBookingForm(data)

            if form.is_valid():
                booking = form.save(commit=False)
                booking.faculty_id = request.user
                booking.department = request.user.department
                booking.status = 'Pending'
                booking.save()

                return JsonResponse({'success': True, 'booking_id': booking.id})

            return JsonResponse({'success': False, 'error': form.errors}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


from django.http import JsonResponse

def check_availability(request):
    # Extract the booking details from the POST request body
    try:
        data = json.loads(request.body)
        lab = data.get('lab')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        # Implement your availability check logic here.
        # For demonstration purposes, let's assume availability is checked.
        available = True  # You'd replace this with your actual logic.
        message = "Lab is available" if available else "Lab is not available"
        
        return JsonResponse({
            'available': available,
            'message': message
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)



@login_required
def lab_booking_list(request):
    return redirect('lab:lab_booking_list')

@login_required
def lab_booking(request):
    return render(request, 'lab/lab_booking.html')

@login_required
def admin_dashboard(request):
    return render(request, 'lab/admin_dashboard.html')

@login_required
def calendar_view(request):
    return render(request, 'lab/calendar.html')

@login_required
def get_events(request):
    bookings = LabBooking.objects.all()
    events = []
    for booking in bookings:
        events.append({
            'id': booking.id,
            'title': booking.event_name,
            'start': booking.start_date.isoformat(),
            'end': booking.end_date.isoformat(),
            'description': booking.event_description,
            'chief_guest': booking.chief_guest,
            'lab': booking.lab,
            'status': booking.status,
            'department': booking.department,
            'coordinator': booking.event_coordinator
        })
    return JsonResponse(events, safe=False)


# ... (other imports)
from django.db.models import Q

# ... (other views)

@login_required
def product_list(request):
    category = request.GET.get('category')
    search_query = request.GET.get('q') # Get the search query

    products = Product.objects.all()

    if category:
        products = products.filter(category=category)

    if search_query: # Filter products if there is a search query
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )


    categories = Product.objects.values_list('category', flat=True).distinct()  # Get distinct categories
    return render(request, 'lab/product_list.html', {'products': products, 'categories': categories, 'selected_category': category, 'search_query': search_query})


# ... (rest of your views.py)|




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser, Product, Order, LabBooking
from .forms import CustomUserForm, ProductForm
from django.db.models import Count

def is_admin(user):
    return user.is_authenticated and user.user_type == 'ADMIN'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_bookings = LabBooking.objects.count()
    
    recent_orders = Order.objects.order_by('-created_at')[:5]
    recent_bookings = LabBooking.objects.order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_bookings': total_bookings,
        'recent_orders': recent_orders,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'admin/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'admin/user_list.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User added successfully.')
            return redirect('lab:user_list')
    else:
        form = CustomUserForm()
    return render(request, 'admin/user_form.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(is_admin)
def update_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('lab:user_list')

    else:
        form = CustomUserForm(instance=user)
    return render(request, 'admin/user_form.html', {'form': form, 'action': 'Update'})

@login_required
@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('lab:user_list')

@login_required
@user_passes_test(is_admin)
def admin_product_list(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'admin/product_list.html', {'products': products})

@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully.')
            return redirect('lab:admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form, 'action': 'Add'})

@login_required
@user_passes_test(is_admin)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('lab:admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form, 'action': 'Update'})

@login_required
@user_passes_test(is_admin)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print("product delete request")
    product.delete()
    print("Product deleted")
    messages.success(request, 'Product deleted successfully.')
    return redirect('lab:admin_product_list')


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q

@login_required
@user_passes_test(is_admin)
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Handle filters
    status_filter = request.GET.get('status')
    product_filter = request.GET.get('product')
    user_filter = request.GET.get('user')
    search_query = request.GET.get('search')
    
    if status_filter:
        orders = orders.filter(order_status=status_filter.upper())
    
    if product_filter:
        orders = orders.filter(product_id=product_filter)
        
    if user_filter:
        orders = orders.filter(user_id=user_filter)
        
    if search_query:
        orders = orders.filter(
            Q(user__username__icontains=search_query) |
            Q(product__name__icontains=search_query) |
            Q(razorpay_order_id__icontains=search_query)
        )
    
    # Get unique products and users for filter dropdowns
    products = Product.objects.all()
    users = CustomUser.objects.all()
    
    context = {
        'orders': orders,
        'products': products,
        'users': users,
        'current_status': status_filter,
        'current_product': product_filter,
        'current_user': user_filter,
        'search_query': search_query
    }
    
    return render(request, 'admin/order_list.html', context)

@login_required
@user_passes_test(is_admin)
def update_order_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            order_id = data.get("order_id")
            new_status = data.get("status")

            # Find the order and update the status
            order = Order.objects.get(id=order_id)
            order.order_status = new_status
            order.save()

            return JsonResponse({"success": True})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "error": "Order not found"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method"})

@login_required
@user_passes_test(is_admin)
def admin_lab_bookings(request):
    bookings = LabBooking.objects.all().order_by('-created_at')
    return render(request, 'admin/lab_booking.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin)
def update_booking_status(request, pk):
    booking = get_object_or_404(LabBooking, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('status')
        booking.status = status
        booking.save()
        messages.success(request, 'Booking status updated successfully.')
    return redirect('admin_lab_bookings')