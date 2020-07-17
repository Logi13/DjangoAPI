# payments/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from djstripe.models import Product
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from website.settings import STRIPE_PUBLISHABLE_KEY, STRIPE_SECRET_KEY

import stripe
import json
import djstripe

@login_required
def homepage(request):
	return render(request, "payments_main.html")

def checkout(request):
	products = Product.objects.all()
	return render(request,"checkout.html", {"products": products})

def complete(request):
    return render(request, "success.html")

def cancelledView(request):
    return   render(request, "cancelled.html")

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@login_required
def create_sub(request):
    if request.method == 'POST':
        # Reads application/json and returns a response
        data = json.loads(request.body)
        payment_method = data['payment_method']
        stripe.api_key = STRIPE_SECRET_KEY
        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)
        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
            payment_method=payment_method,
            email=request.user.email,
            invoice_settings={
                'default_payment_method': payment_method
                }
            )	        
            djstripe_customer = djstripe.models.Customer.sync_from_stripe_data(customer)
            request.user.customer = djstripe_customer
            # At this point, associate the ID of the Customer object with your
            # own internal representation of a customer, if you have one.
            # print(customer)	        # Subscribe the user to the subscription created
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=["latest_invoice.payment_intent"]
            )	        
            djstripe_subscription = djstripe.models.Subscription.sync_from_stripe_data(subscription)	        
            request.user.subscription = djstripe_subscription
            request.user.save()	      
            return JsonResponse(subscription)
        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status = 403)
        else:
            print("!")
            return HTTPresponse('requet method not allowed')
