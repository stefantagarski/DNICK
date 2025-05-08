from django.db.models.signals import *
from django.dispatch import receiver

from flightapp.models import *

@receiver(pre_save, sender=Pilot) # pre_save signal is triggered before saving the Pilot instance
def update_rank_to_pilot(sender, instance, **kwargs):
        if instance.total_flight_hours > 1000:
            instance.rank = "CAPTAIN"
        elif instance.total_flight_hours > 500:
            instance.rank = "FIRST_OFFICER"
        else:
            instance.rank = "SECOND_OFFICER"

@receiver(post_save, sender=Flight) # post_save signal is triggered after saving the Flight instance
def generate_report_after_flight_creation(sender, instance, created, **kwargs):
    if created:
        description = f'Flight {instance.code}:\n' \
                      f'Take-off airport: {instance.take_off_airport}\n' \
                      f'Landing airport: {instance.landing_airport}\n' \
                      f'Balloon: {instance.balloon.name}\n' \
                      f'Pilot: {instance.pilot.first_name} {instance.pilot.last_name}\n' \
                      f'Airline: {instance.airline.name}\n'
        FlightReport.objects.create(flight = instance, description = description)


@receiver(pre_delete, sender=Airline) # pre_delete signal is triggered before deleting the Airline instance
def assign_pilots_after_airline_deletion(sender, instance, **kwargs):
    airline_pilots = AirlinePilot.objects.filter(airline = instance).all()

    new_airline = Airline.objects.exclude(id = instance.id).first()

    for airline_pilot in airline_pilots:
        airline_pilot.airline = new_airline
        airline_pilot.save()

@receiver(post_delete, sender=Airline) # post_delete signal is triggered after deleting the Airline instance
def log_airline_after_deletion(sender,instance, **kwargs):
    AirlineLog.objects.create(
        name=instance.name,
        year_founded=instance.founded_year,
        description=f'Airline {instance.name} is deleted from the system!'
    )
