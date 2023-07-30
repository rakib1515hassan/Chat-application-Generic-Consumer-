from django.urls import path
from ChatApp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/<str:group_name>/', views.Chatting, name='chatting'),
]

