import re
import json
import logging
import urllib.request
import urllib.request

from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather.serializer import WeatherSerializer

# Set up logging
logger = logging.getLogger(__name__)


class WeatherView(View):
    template_name = "main/index.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        try:
            city = request.POST.get("city")
            if not city:
                return render(
                    request, self.template_name, {"error": "Please enter a city name."}
                )

            # Define a pattern that matches any special characters
            special_char_pattern = re.compile(r'[^\w\s]', re.ASCII)

            # Check if the city contains any special characters
            if special_char_pattern.search(city):
                return render(
                    request, self.template_name, {"error": "The city name cannot contain special characters. Please enter a valid city name."}
                )

            api_key = "54cd7391496f42b690a130940243107"
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
            logger.info(f"Requesting URL: {url}")

            response = urllib.request.urlopen(url)
            data = json.loads(response.read())
            logger.info(f"Received response: {data}")

            context = {
                "city": city,
                "country": data["location"]["country"],
                "region": data["location"]["region"],
                "temperature_c": data["current"]["temp_c"],
                "temperature_f": data["current"]["temp_f"],
                "condition": data["current"]["condition"]["text"],
                "icon": data["current"]["condition"]["icon"],
            }
            return render(request, self.template_name, context)
        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return render(
                request, self.template_name, {"error": "Error fetching weather data."}
            )


class WeatherAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = WeatherSerializer(data=request.data)
        if serializer.is_valid():
            city = serializer.validated_data["city"]
            api_key = "54cd7391496f42b690a130940243107"
            url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"
            try:
                response = urllib.request.urlopen(url)
                data = json.loads(response.read())
                context = {
                    "city": city,
                    "country": data["location"]["country"],
                    "region": data["location"]["region"],
                    "temperature_c": data["current"]["temp_c"],
                    "temperature_f": data["current"]["temp_f"],
                    "condition": data["current"]["condition"]["text"],
                    "icon": data["current"]["condition"]["icon"],
                }
                return Response(context, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
