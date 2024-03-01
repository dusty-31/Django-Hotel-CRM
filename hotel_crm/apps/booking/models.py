from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Booking(models.Model):
    hotel = models.ForeignKey(to='hotels.Hotel', on_delete=models.PROTECT)
    customer = models.ForeignKey(to='customers.Customer', on_delete=models.PROTECT)
    room = models.ForeignKey(to='hotels.Room', on_delete=models.PROTECT)
    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='bookings')

    def get_absolute_url(self):
        return reverse(viewname='booking:detail', kwargs={'pk': self.pk})
