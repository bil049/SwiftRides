from django.urls import path
from . import views



urlpatterns = [
    path('', views.loginPage, name="login"),
    path('register/', views.register, name="register"),
    path('companycar/', views.companycar, name= "companycar" ),
    path('rentedcar/', views.rentedcars, name= "rentedcars" ),
    path('logout/', views.logoutUser, name="logout"),
    path('uploadcar/', views.uploadcar, name="uploadcar"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('registration/', views.registration, name="registration"),
    path('cardetails/<int:car_id>/', views.details, name="cardetails"),
    path('updatecar/<int:pk>/', views.update_cardetails, name="updatecar"),
    path('deletecar/<int:pk>/', views.delete_car, name="deletecar"),
    path('updateprofile/<int:pk>/', views.updateprofile, name="updateprofile"),
]