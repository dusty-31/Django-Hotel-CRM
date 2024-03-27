from django import forms

from hotel_crm.apps.hotels.models import Hotel

from .models import Booking
from .selectors import get_available_rooms_by_hotel_id


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'number_of_guests', 'hotel', 'customer', 'room']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date'}),
            'check_out': forms.DateInput(attrs={'type': 'date'}),
            'hotel': forms.Select(attrs={'id': 'hotel_choice'}),
            'room': forms.Select(attrs={'id': 'room_choice'}),
        }

    def __init__(self, created_by, *args, hotel_id=None, **kwargs):
        initial_values = kwargs.get('initial', {})
        initial_values.setdefault('hotel', hotel_id)
        super(BookingForm, self).__init__(*args, **kwargs)
        self.created_by = created_by
        self.fields['hotel'].queryset = Hotel.objects.filter(owner=created_by)
        self.fields['room'].queryset = get_available_rooms_by_hotel_id(hotel_id=hotel_id, order_by=['number', 'type'])

    def save(self, commit=True):
        booking = super(BookingForm, self).save(commit=False)
        booking.created_by = self.created_by
        if commit:
            booking.save()
        return booking

    def clean(self):
        # Check check-in and check-out dates
        check_in = self.cleaned_data['check_in']
        check_out = self.cleaned_data['check_out']
        if check_in >= check_out:
            raise forms.ValidationError('Check-in date must be before check-out date.')

    def clean_room(self):
        room_data = self.cleaned_data['room']
        number_of_guests = self.cleaned_data['number_of_guests']
        if not room_data.is_available:
            raise forms.ValidationError('This room is not available.')
        if number_of_guests > room_data.type.max_occupancy:
            raise forms.ValidationError('Number of guests exceeds room max occupancy.')
        return room_data
