from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .choices import PAYMENT_METHOD, ZONE

class Order(models.Model):
    quantity = models.IntegerField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=255)
    recipient_number = models.CharField(max_length=255)
    recipient_address = models.CharField(max_length=255)
    zone =models.CharField(max_length=8, choices=ZONE)
    order_date = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.sender.username

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    unit_price = models.IntegerField(default=220)
    amount = models.IntegerField()
    method = models.CharField(max_length=8, choices=PAYMENT_METHOD)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.order.sender.username

class Newsletter(models.Model):
    email = models.EmailField()
    time_stamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class ContactUs(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.name