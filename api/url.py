from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('api-token-auth/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('airline/', AirlineView.as_view()),
    path('airline/<int:pk>', UpdateAirlineView.as_view()),
    path('aircraft/', AircraftView.as_view()),
    path('aircraft/<int:pk>', UpdateAircraftView.as_view()),
]
