from django.urls import path
from logis import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('service-details/', views.service_details, name='service_details'),
    path('getaquote/', views.getaquote, name='getaquote'),
    path('starterpage/', views.starterpage, name='starterpage'),
    path('pricing/', views.pricing, name='pricing'),
]
