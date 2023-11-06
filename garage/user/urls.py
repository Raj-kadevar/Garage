from django.contrib.auth.views import LogoutView
from django.urls import path

from user.views import UserLoginView, RegistrationView, VerficationView, HomeView, ResetPassword, CarRegistrationView, \
    BikeRegistrationView, BikeList, CarList, CarUpdate, BikeUpdate, BikeDelete, CarDelete, AddGarage, UpdateGarage, \
    DeleteGarage, AddSchedule, RepairVehicle

urlpatterns = [
    path("index/", HomeView.as_view(), name="index"),
    path("", HomeView.as_view(), name="index"),

    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("registration/", RegistrationView.as_view(), name="registration"),

    path("reset-password/", ResetPassword.as_view(), name="reset_password"),
    path("email-verification/<id>",VerficationView.as_view(),name="email_verification"),

    path("add-bike/", BikeRegistrationView.as_view(), name="add_bike"),
    path("add-car/", CarRegistrationView.as_view(), name="add_car"),
    path("bike-list/", BikeList.as_view(), name="bike_list"),
    path("car-list/", CarList.as_view(), name="car_list"),

    path("update-car/<int:pk>", CarUpdate.as_view(), name="car_update"),
    path("update-bike/<int:pk>", BikeUpdate.as_view(), name="bike_update"),

    path("delete-bike/<int:pk>", BikeDelete.as_view(), name="bike_delete"),
    path("delete-car/<int:pk>", CarDelete.as_view(), name="car_delete"),

    path("add-garage/", AddGarage.as_view(), name="add_garage"),
    path("update-category/<int:pk>", UpdateGarage.as_view(), name="update_garage"),
    path("delete-garage/<int:pk>", DeleteGarage.as_view(), name="delete_garage"),

    path("add-schedule/", AddSchedule.as_view(), name="add_schedule"),
    path("repair-vehicle/", RepairVehicle.as_view(), name="repair-vehicle"),
]