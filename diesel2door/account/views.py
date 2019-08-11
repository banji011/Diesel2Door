from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from diesel.models import Order, Payment


def register(request):
    registered = False 
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.phone = form.cleaned_data.get('phone')
            user.profile.address = form.cleaned_data.get('address')
            user.save()
            registered = True
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Account created for {username}! ')
            send_mail(
                        'Welcome Onboard',
                        f'''
                        
                        Hello {username}
                        Your account has been created successfully. 
                        Stay tuned for any change in AGO price
                         ''',
                        'Crestfield Diesel2Door',
                        [email],
                        fail_silently=False,
                    )
            return redirect('login')
        else:
            messages.warning(request,f' {form.errors} ')
            print( form.errors)

    else:
        form = UserRegisterForm()
    return render(request, 'account/register.html',{'form':form, 'registered':registered})


@login_required
def profile(request):
    orders = Order.objects.filter(sender=request.user).all()
    return render(request, 'account/profile.html',{'orders':orders})


