from django.contrib import admin


from .models import Order, Payment, ContactUs, Newsletter

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(ContactUs)
admin.site.register(Newsletter)

