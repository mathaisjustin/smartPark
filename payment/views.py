from django.shortcuts import render, redirect

# Create your views here.
import razorpay
from .models import Subscriptions
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100
        print(name)
        print(amount)
        client = razorpay.Client(
            auth=("rzp_test_XHGmRIczlc1NSe", "DFGObQ52tiEM3KP2wPDqDY56"))
        payment = client.order.create(
            {'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        # print(payment)
        sub = Subscriptions(name=name, amount=amount,
                            payment_id=payment['id'])
        sub.save()
        return render(request, 'payment.html',  {'payment': payment})
    return render(request, 'payment.html')


@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        # print(a)
        order_id = ""
        data = {}
        for key, val in a.items():
            if key == 'razorpay_order_id':
                data['order_id'] = val
                order_id = val
            elif key == 'razorpay_payment_id':
                data['payment_id'] = val
            elif key == 'razorpay_signature':
                data['signature'] = val
        # print(order_id)
        user = Subscriptions.objects.filter(payment_id=order_id).first()
        user.paid = True
        user.save()
        # return redirect('payment/success/')
        # if (user.paid == True):
        #     return redirect('/payments/success/')
        # else:
        #     pass
        # return render(request, 'failure.html')
    return render(request, 'userdetails.html')
