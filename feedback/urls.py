from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_form, name='feedback_form'),
    path('thank_you/', views.thank_you, name='thank_you'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard-data/', views.dashboard_data, name='dashboard_data'),
]
