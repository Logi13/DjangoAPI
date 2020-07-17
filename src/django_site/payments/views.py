# payments/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from djstripe.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 

import stripe
import json

def homepage(request):
	return render(request, "payments_main.html")@login_required

def checkout(request):
	products = Product.objects.all()
	return render(request,"checkout.html",{"products": products})

def successView(request):
    return render(request, "success.html")

def cancelledView(request):
    return render(request, "cancelled.html")

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
                # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payments/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payments/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Premium Cat Picture',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def create_subscription(request):
    data = json.loads(request.data)
    try:
        # Attach the payment method to the customer
        stripe.PaymentMethod.attach(
            data['paymentMethodId'],
            customer=data['customerId'],
        )
        # Set the default payment method on the customer
        stripe.Customer.modify(
            data['customerId'],
            invoice_settings={
                'default_payment_method': data['paymentMethodId'],
            },
        )

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=data['customerId'],
            items=[
                {
                    'price': 'price_HGd7M3DV3IMXkC'
                }
            ],
            expand=['latest_invoice.payment_intent'],
        )
        return jsonify(subscription)
    except Exception as e:
        return jsonify(error={'message': str(e)}), 200

def checkout(request):
    if request.method == 'GET':
        domain_url = DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
                # Create new Checkout Session for the order
        # Other optional params include:
        # [billing_address_collection] - to display billing address details on the page
        # [customer] - if you have an existing Stripe Customer ID
        # [payment_intent_data] - lets capture the payment later
        # [customer_email] - lets you prefill the email input in the form
        # For full details see https:#stripe.com/docs/api/checkout/sessions/create

        # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payments/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payments/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Premium Cat Picture',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

# @app.route('/create-customer', methods=['POST'])
def create_customer():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Reads application/json and returns a response
    data = json.loads(request.data)
    try:
        # Create a new customer object
        customer = stripe.Customer.create(
            email="johnny.lioup@gmail.com"#data['email']
        )
        # At this point, associate the ID of the Customer object with your
        # own internal representation of a customer, if you have one.

        return jsonify(
            customer=customer,
        )
    except Exception as e:
        return jsonify(error=str(e)), 403