from django import forms

from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['hotel', 'customer', 'room', 'check_in', 'check_out', 'number_of_guests']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'hotel': forms.Select(attrs={'id': 'hotel_choice'}),
            'room': forms.Select(attrs={'id': 'room_choice'}),
        }
