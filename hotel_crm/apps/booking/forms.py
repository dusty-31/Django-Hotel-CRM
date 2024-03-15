from django import forms

from hotel_crm.apps.customers.models import Customer
from hotel_crm.apps.hotels.models import Hotel, Room

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

    def clean(self):
        # Check check-in and check-out dates
        check_in = self.cleaned_data['check_in']
        check_out = self.cleaned_data['check_out']
        if check_in >= check_out:
            raise forms.ValidationError('Check-in date must be before check-out date.')

    def clean_room(self):
        room_data = self.cleaned_data['room']
        if not room_data.is_available:
            raise forms.ValidationError('This room is not available.')
        return room_data

    def clean_number_of_guests(self):
        number_of_guests = self.cleaned_data['number_of_guests']
        room = self.cleaned_data['room']
        if number_of_guests > room.type.max_occupancy:
            raise forms.ValidationError('Number of guests exceeds room max occupancy.')
        return number_of_guests


class BookingWithCustomerForm(forms.Form):
    # Customer fields
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    phone_number = forms.CharField(max_length=15)
    gender = forms.ChoiceField(choices=Customer.GENDER_CHOICES)
    passport_number = forms.CharField(max_length=14)
    disability = forms.BooleanField(required=False)

    # Booking fields
    hotel = forms.ModelChoiceField(
        queryset=Hotel.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'hotel_choice',
            }
        ),
    )
    room = forms.ModelChoiceField(
        queryset=Room.objects.all(),
        widget=forms.Select(
            attrs={
                'id': 'room_choice',
            }
        ),
    )
    check_in = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
        ),
    )
    check_out = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            },
        ),
    )
    number_of_guests = forms.IntegerField()
