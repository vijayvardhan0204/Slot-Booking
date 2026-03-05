from django.db import models
from django.utils.timezone import now

# Create your models here.
class Slot(models.Model):
    date = models.DateField(default=now)
    time = models.TimeField()
    is_booked = models.BooleanField(default=False)
    booked_by = models.CharField(max_length=100,null=True,blank=True)

    class Meta:
        unique_together = ('date', 'time')

def __str__(self):
    return self.slot_time