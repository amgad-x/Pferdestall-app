from django.urls import path
from . import views

urlpatterns = [
    path('', views.startseite, name='startseite'),
    path('hinzufuegen/', views.pferd_hinzufuegen, name='pferd_hinzufuegen'),
    path('liste/', views.pferd_liste, name='pferd_liste'),
    path('details/<int:pk>/', views.pferd_details, name='pferd_details'),
    path('bearbeiten/<int:pk>/', views.pferd_bearbeiten, name='pferd_bearbeiten'),
    path('loeschen/<int:pk>/', views.pferd_loeschen, name='pferd_loeschen'),
    path('zugang/', views.zugangskontrolle, name='zugangskontrolle'),
    path('bearbeiten/<int:pk>/', views.pferd_bearbeiten, name='pferd_bearbeiten'),
    path("api/zugangskontrolle/", views.zugang_api, name="zugang_api"),

]

