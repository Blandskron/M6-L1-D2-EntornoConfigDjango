from django.urls import path

from . import views

app_name = 'configuracion'

urlpatterns = [
    path('', views.home, name='home'),
    path('entorno/', views.entorno, name='entorno'),
    path('db/', views.db, name='db'),
]
