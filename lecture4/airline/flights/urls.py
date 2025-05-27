from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('<int:flight_id>', views.flight, name="flight")
]