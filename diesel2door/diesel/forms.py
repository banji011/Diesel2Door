from django import forms
from .models import Order, Payment
from django.contrib.auth.models import User 
from .choices import PAYMENT_METHOD, ZONE

class OrderForm(forms.Form):
    quantity = forms.IntegerField(label='Quantity', min_value=500)
    recipient_name = forms.CharField(label='Recipient Name', max_length=100)
    recipient_number = forms.CharField(label='Recipient Number', max_length=12)
    recipient_address = forms.CharField(label='Recipient Address', max_length=100)
    zone = forms.CharField(max_length=8,widget=forms.Select(choices=ZONE))

class PaymentForm(forms.Form):
    method =forms.CharField(max_length=8,widget=forms.Select(choices=PAYMENT_METHOD))


class NewsletterForm(forms.Form):
    email = forms.CharField(max_length=100,
                            widget=forms.EmailInput(attrs={'type':'email','class':'form-control', 'placeholder':'Enter your email','class':'form-control'}))

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'Your name'}))
    email = forms.CharField(max_length=100,
                            widget=forms.EmailInput(attrs={'type':'email','class':'form-control','placeholder':'Your email'}))
    subject = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={'type':'text','class':'form-control','placeholder':'Subject'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Your message','rows':'5'}))                    


