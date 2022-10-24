
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('chat/',views.chat, name="chat"),
    path('message/<str:q>/ajax/',views.ajax, name ="ajax"),
    path('message/<str:q>/',views.message, name="message")
]
