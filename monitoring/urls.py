
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('prediction/', views.new_prediction, name='new_prediction'),
    path('history/', views.prediction_history, name='prediction_history'),
    path('chart/', views.rul_chart, name='rul_chart'),
]