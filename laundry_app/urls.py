from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track/', views.track_order, name='track_order'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
