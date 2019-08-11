from __future__ import unicode_literals
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, PaymentForm, NewsletterForm, ContactUsForm
from .models import Order, Payment, Newsletter, ContactUs
from django.contrib import messages
from django.core.mail import send_mail
import requests


def homepage(request):
    if request.method == 'POST':
        newsform = NewsletterForm(request.POST, prefix='news')
        if newsform.is_valid():
            email = newsform.cleaned_data['email']
            new_letter = Newsletter(email=email)
            new_letter.save()
        else:
            print(newsform.errors)
    else:
        newsform = NewsletterForm(prefix='news')


    if request.method == 'POST' and not newsform.is_valid():
        contactform = ContactUsForm(request.POST, prefix='contact')
        newsform = NewsletterForm(prefix='news')
        if contactform.is_valid():
            name = contactform.cleaned_data['name']
            email = contactform.cleaned_data['email']
            subject = contactform.cleaned_data['subject']
            message = contactform.cleaned_data['message']
            new_contact = ContactUs(name=name,email=email,subject=subject,message=message)
            new_contact.save()
        else:
            print(contactform.errors)
    else:
        contactform = ContactUsForm(prefix='contact')
        
    return render(request, 'diesel/index.html', {'title': 'Homepage','newsform':newsform,'contactform':contactform}) 

@login_required
def order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
           quantity = form.cleaned_data['quantity']
           recipient_name = form.cleaned_data['recipient_name']
           recipient_number = form.cleaned_data['recipient_number']
           recipient_address = form.cleaned_data['recipient_address']
           zone = form.cleaned_data['zone'] 
           print(quantity)
           print(recipient_name)
           print(recipient_number)
           print(recipient_address)
           print(request.user)
           new_order = Order(quantity=quantity,sender=request.user,recipient_name=recipient_name,recipient_number=recipient_number,recipient_address=recipient_address,zone=zone)
           new_order.save()
           request.session['order_id'] = new_order.id
           send_mail(
                        'Order Placed',
                        f''' 
                        Hello {request.user}
                        Your order for {quantity} litres of AGO has bee received
                        Pls verify order to continue
                         ''',
                        'Crestfield Diesel2Door',
                        [request.user.email],
                        fail_silently=False,
                    )
           requests.post(f"http://www.smsmobile24.com/index.php?option=com_spc&comm=spc_api&username=MZYF&password=MZYFS&sender=Crestfield&recipient={request.user.profile.phone}&message=Your Order of {quantity} of AGO has been placed. &")
           return redirect('verify_order')
        else:
            print(form.errors)
    else:
        form = OrderForm()

    return render(request, 'diesel/ordernow.html', {'form':form})


@login_required
def verify_order(request):
    order_id = request.session.get('order_id')
    the_order = get_object_or_404(Order,id=order_id)
    print(the_order.sender.username)
    unit_price = 220
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            method = form.cleaned_data['method']
            if method == 'TRANSFER':
                print(the_order.quantity)
                amount = the_order.quantity * unit_price
                new_payment = Payment(order=the_order,amount=amount,method=method)
                new_payment.save()
                the_order.completed = True
                the_order.save()
                date = the_order.order_date.strftime("%Y%m%d")
                send_mail(
                        'Order Successful',
                        f''' 
                        
                        Hello {request.user}
                        Thank You For Your Order 
                        ORDER DETAILS  
                        {the_order.order_date}
                        Volume Ordered: {the_order.quantity} 
                        Price/Litre: NGN220
                        Total: NGN{amount}


                        DELIVERY DETAILS 
                         {the_order.recipient_name}
                         {the_order.recipient_address}
                         {the_order.recipient_number}
                         {the_order.zone}


                         PAYMENT OPTIONS AND DETAILS 
                        
                        Wire Transfer
                        Order Reference: {request.user}{date}
                        
                        While we process your order, we await your payment confirmation 

                        Please find below our account details
                        Account name: Crestfield Energy Resources 
                        Account number: **********
                        Bank: FCMB 


                        Send payment evidence to orders@crestfieldenergy.com and our customer service rep will contact you. 

                        Regards 
                        Crestfield Energy Resources 

                         ''',
                        'Crestfield Diesel2Door',
                        [request.user.email],
                        fail_silently=False,
                    )
                return redirect('order_successful')
            elif method == 'CARD':
                messages.info(request, 'No Card Option Available yet, Pls continue with wire transfer! ')
                amount = the_order.quantity * unit_price
                new_payment = Payment(order=the_order,amount=amount,method=method)
                new_payment.save()
                the_order.completed = True
                the_order.save()
                return redirect('homepage')
        else:
            print(form.errors)
    else:
        form = PaymentForm()
    return render(request,'diesel/verify_order.html',{'form':form, 'the_order':the_order})
            
@login_required
def order_successful(request):
    return render(request,'diesel/order_successful.html')

