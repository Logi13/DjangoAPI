# payments/urls.py

from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.homepage, name='payments'),
    path('config/', views.stripe_config),

    path('checkout/', views.checkout),
    path('cancelled/', views.cancelledView),
	path("create-sub", views.create_sub, name="create sub"), #add
	path("complete", views.complete, name="complete"), #add

]