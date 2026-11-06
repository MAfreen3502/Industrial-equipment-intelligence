from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_rul_api, name='predict-rul'),
]