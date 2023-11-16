from django.contrib import admin
from django.urls import include, path
from . import views



app_name = "houses"
urlpatterns = [
    path('', views.home, name ='home'),
    path('houselist/', views.list_house, name='list_house'),
    path('edit/', views.edit_house, name='edit_house'),
    path('delete/', views.remove_house, name='remove_house'),
    path('delete/process', views.remove_process, name='remove_process'),
    path('edit/process', views.edit_process, name='edit_process'),
    path('sell/', views.sell_house, name='sell_house'),
    path('sell/process', views.sell_process, name='sell_process'),

]