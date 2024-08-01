# weather/urls.py
from django.urls import path

from weather.views import WeatherView, WeatherAPIView

urlpatterns = [
    path('', WeatherView.as_view(), name='index'),
    path('api/weather/', WeatherAPIView.as_view(), name='weather-api'),

]

