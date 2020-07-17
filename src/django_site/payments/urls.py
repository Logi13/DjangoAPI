# payments/urls.py

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.homepage, name='payments'),
    path('config/', views.stripe_config),
    path('checkout/', views.checkout),
    path('create_subscription', views.create_subscription),
    path('create-checkout-session/', views.create_checkout_session),
    path('success/', views.successView),
    path('cancelled/', views.cancelledView),
    # endpoints
    re_path(r'^create_customer[/]?$', views.create_customer),
]