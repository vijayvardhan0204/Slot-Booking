from django.contrib import admin
from .models import Slot

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ("date", "time", "is_booked", "booked_by")
    list_filter = ("date", "is_booked")