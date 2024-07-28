from django.urls import path
from . import views


urlpatterns = [
    path('', views.userlogin, name="userlogin"),
    path('register/', views.userregister, name="userregister"),
    path('userregistration/', views.userregistration, name="userregistration"),
    path('home/', views.index, name="index"),
    path('logout/', views.logoutUser, name="logoutuser"),
    path('companycars/<str:company_name>/', views.company_cars, name='company_cars'),
    path('rentcar/<int:car_id>/<str:company_name>/', views.rentcar, name="rentcar"),
    path('rentalcompanies/', views.rentalcompanies, name ="rentalcompanies"),
    path('cardetails/<int:car_id>/', views.singlecar, name="singlecar"),
    path('updateaccount/<int:pk>/', views.updateaccount, name="updateaccount"),
    path('updatereservation/<int:pk>/', views.updatereservation, name="updatereservation"),
    path('userdashboard/', views.userdashboard, name="userdashboard"),
    path('reservation/<int:reservation_id>/cancel/', views.cancelreservation, name='cancelreservation'),
    path('initiatepayment/', views.initiate_payment, name="initiatepayment"),
    path('<str:reference>', views.verify_payment, name="verifypayment"),
    path('available/', views.available_cars, name="availablecars")
]