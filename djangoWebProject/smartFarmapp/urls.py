from django.contrib import admin
from django.urls import path, include
from smartFarmapp import views

urlpatterns = [
    path('', views.home, name='home' ),
    path('signUp/', views.signUp, name='signUp' ),
]