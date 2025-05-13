from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import ContactForm, FlightForm
from .models import Flight
from datetime import datetime

# Create your views here.
def index(request):
    flights = Flight.objects.filter(date__lte = datetime.now().date())
    context = {'flight_list': flights, 'app_name': 'flightapp'}
    return render(request, 'index.html', context)

def details(request, flight_id):
    flight = Flight.objects.filter(id = flight_id).first()
    context = {'flight_data': flight, 'app_name': 'flightapp'}
    return render(request, 'details.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            # Process the data as needed
            return redirect('index')

    form = ContactForm()
    return  render(request, "contact.html", {'form': form})

def add_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('index')

    form = FlightForm()
    return render(request, "add_flight.html", context={'form': form})

def edit_flight(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    # Flight.objects.filter(pk=flight_id).exists()

    if request.method == 'POST':
        form = FlightForm(request.POST, request.FILES, instance=flight)
        if form.is_valid():
            form.save()

        return redirect('index')

    form = FlightForm(instance=flight)
    return render(request, "edit_flight.html", context={'form': form, 'flight_id': flight_id})