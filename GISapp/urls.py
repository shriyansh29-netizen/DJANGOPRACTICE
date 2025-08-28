from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feeders/', views.feeder_list, name='feeder_list'),
    path('feeders/delete/<int:pk>/', views.feeder_delete, name='feeder_delete'),
    path("dts/", views.dt_list, name="dt_list"),
    path("dts/delete/<int:dt_id>/", views.dt_delete, name="dt_delete"),
    path("loc/", views.location_form, name="location_form"),
    path('feeder-dt/', views.feeder_dt_select, name='feeder_dt_select'),
    path('ajax/get-dts/', views.ajax_get_dts, name='ajax_get_dts'),
    path("show-feeder-dt/", views.show_feeder_dt_data, name="show_feeder_dt_data"),


]
