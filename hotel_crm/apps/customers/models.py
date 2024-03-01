from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    passport_number = models.CharField(max_length=14)  # Example: 12345678-12345
    disability = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - created by {self.created_by.username}'

    def get_absolute_url(self):
        return reverse(viewname='customers:detail', kwargs={'pk': self.pk})
