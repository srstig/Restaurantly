
from django.contrib import admin
from django.urls import path
from cafeapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('starter/', views.starter, name='starter'),
    path('about/', views.about, name='about'),
    path('booking/', views.booking, name='booking'),
    path('chefs/', views.chefs, name='chefs'),
    path('contact/', views.contact, name='contact'),
    path('events/', views.events, name='events'),
    path('gallery/', views.gallery, name='gallery'),
    path('menu/', views.menu, name='menu'),
    path('specials/', views.specials, name='specials'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('whyus/', views.whyus, name='whyus'),
]
