from django.test import TestCase
from flightapp.models import Pilot, Airline, Balloon, Flight, FlightReport, AirlinePilot


class FlightManagementTestCase(TestCase):
    def setUp(self):
        self.pilot1 = Pilot.objects.create(
            first_name='John', last_name='Doe', total_flight_hours=300, rank='SECOND_OFFICER', birth_year=2001
        )
        self.pilot2 = Pilot.objects.create(
            first_name='Jane', last_name='Smith', total_flight_hours=800, rank='FIRST_OFFICER', birth_year=2001
        )
        self.pilot3 = Pilot.objects.create(
            first_name='Alice', last_name='Johnson', total_flight_hours=1500, rank='CAPTAIN', birth_year=2001
        )
        self.airline1 = Airline.objects.create(
            name='TestAirline', founded_year=1990, is_flying_outside_Europe=False
        )
        self.airline2 = Airline.objects.create(
            name='MacedoniaAirline', founded_year=2001, is_flying_outside_Europe=True
        )
        self.balloon = Balloon.objects.create(
            name='GasBalloon', manufacturer='GasBalloonInc', balloon_type='GAS', capacity=5
        )

    def test_pre_save_signal_pilot_update_rank(self):
        self.pilot1.total_flight_hours = 250
        self.pilot1.save()
        self.assertEqual(self.pilot1.rank, 'SECOND_OFFICER')

        self.pilot1.total_flight_hours = 700
        self.pilot1.save()
        self.assertEqual(self.pilot1.rank, 'FIRST_OFFICER')

        self.pilot1.total_flight_hours = 1500
        self.pilot1.save()
        self.assertEqual(self.pilot1.rank, 'CAPTAIN')

    def test_generate_report_after_flight_creation(self):
        flight = Flight.objects.create(
            code='456789',
            pilot=self.pilot1,
            airline=self.airline1,
            balloon=self.balloon,
        )
        report_exists = FlightReport.objects.filter(flight=flight).exists()
        self.assertTrue(report_exists)

    def test_assign_pilots_after_airline_deletion(self):
        AirlinePilot.objects.create(airline=self.airline1, pilot=self.pilot1)
        AirlinePilot.objects.create(airline=self.airline1, pilot=self.pilot2)
        AirlinePilot.objects.create(airline=self.airline1, pilot=self.pilot3)

        self.airline1.delete()

        pilots_count = AirlinePilot.objects.filter(airline=self.airline2).count()
        self.assertEqual(pilots_count, 3)