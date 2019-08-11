from django.urls import path
from . import views 

urlpatterns = [
    path('', views.homepage, name='homepage'), 
    path('order/', views.order, name='order'),
    path('order/verify_order/', views.verify_order, name='verify_order'),  
    path('order/order_successful/', views.order_successful, name='order_successful'),    
]

