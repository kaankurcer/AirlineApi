from rest_framework import serializers
from .models import *

#Serializer for the user model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs= { 'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

#Serializer for the aircraft model
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ("manufacturer_serial_number", "type", "model", "operator_airline", "number_of_engines")

#Serializer for the airline model
class AirlineSerializer(serializers.ModelSerializer):
    aircraft_set = AircraftSerializer(many=True, required=False)
    class Meta:
        model = Airline
        fields = ("name", "callsign", "founded_year", "base_airport", "aircraft_set")
