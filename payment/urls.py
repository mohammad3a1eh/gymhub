# Github.com/Rasooll
from django.urls import path
from . import views

urlpatterns = [
    path('request/<int:purchase_request_id>/', views.send_request, name='payment_request'),
    path('verify/', views.verify_payment, name='payment_verify'),
]