from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manager-login/', views.manager_login, name='manager-login'),
    path('director-login/', views.director_login, name='director-login'),
    path('manager/', views.manager, name='manager'),
    path('director/', views.director, name='director'),
    path('audience/', views.audience, name='audience'),
    path('audience-login/', views.audience_login, name='audience-login'),
]