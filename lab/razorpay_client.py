import razorpay
from django.conf import settings
class RazorpayClient:
    def __init__(self):
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        self.currency = settings.RAZORPAY_CURRENCY

    def create_order(self, amount, payment_capture=1):
        try:
            data = {'amount': int(amount * 100), 'currency': self.currency, 'payment_capture': payment_capture}
            return self.client.order.create(data)
        except Exception as e:
            print(f"Razorpay Order Creation Error: {e}")
            return None

    def verify_payment_signature(self, payment_data):
        try:
            self.client.utility.verify_payment_signature(payment_data)
            return True
        except Exception as e:
            print(f"Signature Verification Error: {e}")
            return False
