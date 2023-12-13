import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError

# Create your models here.

#Model for a user of the app
class User(AbstractUser):
    username = models.CharField(max_length = 255, unique=True)
    password = models.CharField(max_length = 255)

    REQUIRED_FIELDS=[username,password]

#Model for an airline
class Airline(models.Model):

    #A check to see if the year input is valid
    def validate_founded_year(value):
        cur_year = datetime.date.today()
        cur_year = cur_year.year
        if not (1903 <= value <= cur_year):
            raise ValidationError('Founded year must be a valid year.')
        
    #A check to see if the callsign is valid
    def validate_callsign(value):
        if not (len(value) == 3):
            raise ValidationError('Callsign must be exactly 3 letters long.')
        
    name = models.CharField(max_length=255, unique=True)
    callsign = models.CharField(max_length=255, unique=True)
    founded_year = models.IntegerField(validators=[validate_founded_year])
    base_airport = models.CharField(max_length=255, validators=[validate_callsign])

    def __str__(self):
        return str(self.name)

#Model for an aircraft
class Aircraft(models.Model):
    manufacturer_serial_number = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    operator_airline = models.ForeignKey(Airline, on_delete=models.SET_NULL, null=True) 
    number_of_engines = models.IntegerField()

    def __str__(self):
        return str(self.model)