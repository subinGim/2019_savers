from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# app_name = "mypage_app"

urlpatterns = [
    path('',views.mypage,name="mypage"),
    path('mydetail/',views.mydetail,name="mydetail"),
    # path('<int:p_id>/basket', views.basket, name="basket"), 
    path('basket/<int:pk>', views.basket, name="basket"), 
]

