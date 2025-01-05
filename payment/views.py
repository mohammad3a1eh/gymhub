from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from typing import Dict, Union
import requests
import json
from shop.models import PurchaseRequest
from django.shortcuts import get_object_or_404

def sandbox():
    if settings.SANDBOX:
        return "sandbox"
    else:
        return "payment"
  
def send_request(request, purchase_request_id):

    purchase_request = get_object_or_404(PurchaseRequest, id=purchase_request_id)

    # chack payment status
    if purchase_request.is_paid:
        return redirect(reverse('home'))


    amount = purchase_request.price
    description = f"#{purchase_request.id} : {purchase_request.user.first_name} {purchase_request.user.last_name}"
    mobile = purchase_request.user.phone_number
    email = purchase_request.user.email

    request_url = f"https://{sandbox()}.zarinpal.com/pg/v4/payment/request.json"
    request_data = {
        "merchant_id": settings.MERCHANT,
        "amount": int(amount),
        "callback_url": settings.ZARINPAL_CALLBACK_URL,
        "description": description,
        "currency": "IRR",
        "metadata": {
            "mobile": mobile,
            "email": email,
            "order_id": str(purchase_request_id),
        }
    }
    request_header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    res = requests.post(url=request_url, data=json.dumps(request_data), headers=request_header)
    data = res.json()
    #     {
    #   "data": {
    #     "code": 100,
    #     "message": "Success",
    #     "authority": "A0000000000000000000000000000wwOGYpd",
    #     "fee_type": "Merchant",
    #     "fee": 100
    #   },
    #   "errors": []
    # }

    print(data)
    if data['data']['code'] == 100:
        request.session['amount'] = int(amount)
        request.session['purchase_request_id'] = purchase_request_id
        return redirect(f"https://{sandbox()}.zarinpal.com/pg/StartPay/{data['data']['authority']}")
    else:
        return HttpResponse("errors: " + str(data['errors']))


def verify_payment(request):
    authority = request.GET.get('Authority')
    status = request.GET.get('Status')
    if status == 'OK':
        verify_url = f"https://{sandbox()}.zarinpal.com/pg/v4/payment/verify.json"
        verify_data = {
            "merchant_id": settings.MERCHANT,
            "amount": request.session['amount'],
            "authority": authority,
        }
        verify_header = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        res = requests.post(url=verify_url, data=json.dumps(verify_data), headers=verify_header)
        data = res.json()
        print("*"*12)
        print(data)
        print("*"*12)
        if data['data']['code'] >= 100 and data['data']['code'] < 200:
            purchase_request = get_object_or_404(PurchaseRequest, id=request.session['purchase_request_id'])

            purchase_request.is_paid = True
            purchase_request.save()

            
            return redirect(reverse('home'))
        else:
            # redirect to payment page again with error message path('request/<int:purchase_request_id>/', views.send_request, name='payment_request'),
            return redirect(reverse('payment_request', kwargs={'purchase_request_id': request.session['purchase_request_id']}) + "?error=True")
    else:
        return redirect(reverse("home"))
    

    
