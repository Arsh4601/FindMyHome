from django.contrib import admin
from django.urls import path
from findmyhome import views

urlpatterns = [
    path('', views.home,name="home"),
    path('about', views.about,name="about"),
    path('feedback', views.feed,name="feed"),
    path('result', views.result,name="result"),


]