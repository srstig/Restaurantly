
from django.contrib import admin
from django.urls import path
from cafeapp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('starter/', views.starter, name='starter'),
    path('about/', views.about, name='about'),
]
