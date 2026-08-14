from django.urls import path
from . import views

urlpatterns = [
    path('order/<uuid:template_id>/', views.create_order, name='create_order'),
    path('verify/', views.payment_verify, name='payment_verify'),
]
