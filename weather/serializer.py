from rest_framework import serializers
import re

# Define the custom validator function
def validate_city(value):
    special_char_pattern = re.compile(r'[^\w\s]', re.ASCII)
    if special_char_pattern.search(value):
        raise serializers.ValidationError("The city name cannot contain special characters. Please enter a valid city name.")
    return value

class WeatherSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100, validators=[validate_city])
