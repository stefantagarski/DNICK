from django.contrib import admin

from flightapp.models import *

# Register your models here.

class AirlinePilotInline(admin.TabularInline):
    model = AirlinePilot
    extra = 0

class AirlineAdmin(admin.ModelAdmin):
    inlines = [AirlinePilotInline]
    list_display = ('name', 'founded_year', 'is_flying_outside_Europe')

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

class FlightAdmin(admin.ModelAdmin):
    exclude = ('user',)

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj = None):
        if obj and obj.user == request.user:
            return True
        return False

    def has_delete_permission(self, request, obj = ...):
        return False

class PilotAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')

    def has_delete_permission(self, request, obj = None):
        return False

    def has_change_permission(self, request, obj = None):
        if request.user.is_superuser:
            return True
        return False

admin.site.register(Pilot, PilotAdmin)
admin.site.register(Balloon)
admin.site.register(Airline, AirlineAdmin)
admin.site.register(Flight, FlightAdmin)