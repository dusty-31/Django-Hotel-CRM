from django import forms

from .models import Booking
from .selectors import get_available_hotels_by_dates, get_available_rooms


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer', 'check_in', 'check_out', 'number_of_guests', 'hotel', 'room']
        widgets = {
            'check_in': forms.DateInput(attrs={'id': 'check_in', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'id': 'check_out', 'type': 'date'}),
            'number_of_guests': forms.NumberInput(attrs={'id': 'number_of_guests'}),
            'hotel': forms.Select(attrs={'id': 'hotel_choice'}),
            'room': forms.Select(attrs={'id': 'room_choice'}),
        }

    def __init__(
        self,
        created_by,
        customer_id,
        *args,
        hotel_id=None,
        check_in=None,
        check_out=None,
        number_of_guests=None,
        **kwargs,
    ):
        initial_values = kwargs.get('initial', {})
        initial_values.setdefault('hotel', hotel_id)
        initial_values.setdefault('customer', customer_id)
        initial_values.setdefault('check_in', check_in)
        initial_values.setdefault('check_out', check_out)
        initial_values.setdefault('number_of_guests', number_of_guests)

        super(BookingForm, self).__init__(*args, **kwargs)

        self.created_by = created_by
        self.fields['hotel'].queryset = get_available_hotels_by_dates(
            owner=created_by,
            check_in=check_in,
            check_out=check_out,
            order_by=['name'],
        )
        self.fields['room'].queryset = get_available_rooms(
            hotel_id=hotel_id, number_of_guests=number_of_guests, order_by=['number', 'type']
        )

    def save(self, commit=True) -> Booking:
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
