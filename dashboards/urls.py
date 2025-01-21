from django.urls import path
from dashboards import views

urlpatterns = [
    path('', views.teste, name='teste'),
]
