from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Pilot(models.Model):
    RANKS = [
        ("CAPTAIN", "Captain"),
        ("FIRST_OFFICER", "First Officer"),
        ("SECOND_OFFICER", "Second Officer"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_year = models.IntegerField()
    total_flight_hours = models.IntegerField()
    rank = models.CharField(max_length=20, choices=RANKS, default=RANKS[0])

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.rank})"

class Balloon(models.Model):
    BALLOON_TYPES = [
        ("HOT_AIR", "Hot Air Balloon"),
        ("GAS", "Gas Balloon"),
        ("HYBRID", "Hybrid Balloon"),
    ]
    name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    balloon_type = models.CharField(max_length=20, choices=BALLOON_TYPES, default="HOT_AIR")
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.balloon_type})"

class Airline(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    is_flying_outside_Europe = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class AirlinePilot(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.airline} - {self.pilot}"


class Flight(models.Model):
    code = models.CharField(max_length=10)
    airport_take_off = models.CharField(max_length=100)
    airport_landing = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='flight_images/', blank=True, null=True)
    balloon = models.ForeignKey(Balloon, on_delete=models.CASCADE)
    pilot = models.ForeignKey(Pilot, on_delete=models.CASCADE)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.code} ({self.airport_take_off} - {self.airport_landing})"