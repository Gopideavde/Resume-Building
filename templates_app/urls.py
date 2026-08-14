from django.urls import path
from . import views

urlpatterns = [
    path('', views.template_list, name='template_list'),
    path('<uuid:template_id>/use/', views.use_template, name='use_template'),
]
