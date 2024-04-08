from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .selectors import get_current_customer_bookings, get_future_customer_bookings


class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    INHABITED_CHOICES = [
        ('occupied', 'Occupied'),
        ('unoccupied', 'Unoccupied'),
        ('booked', 'Booked'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    passport_number = models.CharField(max_length=14)  # Example: 12345678-12345
    disability = models.BooleanField(default=False)
    created_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} - created by {self.created_by.username}'

    @property
    def is_inhabited(self) -> str:
        future_bookings = get_future_customer_bookings(customer_id=self.id).exists()
        current_bookings = get_current_customer_bookings(customer_id=self.id).exists()
        if not future_bookings and not current_bookings:
            return self.INHABITED_CHOICES[1][0]
        elif current_bookings:
            return self.INHABITED_CHOICES[0][0]
        elif future_bookings:
            return self.INHABITED_CHOICES[2][0]

    def get_absolute_url(self) -> str:
        return reverse(viewname='customers:detail', kwargs={'pk': self.pk})
