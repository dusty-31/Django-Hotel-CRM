from django import forms

from .models import Hotel, HotelType, Amenities, RoomType


class HotelCreateForm(forms.ModelForm):
    hotel_type = forms.ModelChoiceField(
        queryset=HotelType.objects.all(),
        empty_label='Select hotel type',
    )
    amenities = forms.ModelMultipleChoiceField(
        queryset=Amenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Hotel
        fields = (
            'name',
            'hotel_type',
            'amenities',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for room_type in RoomType.objects.all():
            room_type_name = room_type.name.lower().replace(' ', '_')
            count_field_name = f'{room_type_name}_count'
            self.fields[count_field_name] = forms.IntegerField(
                label=f'Number of {room_type.name} rooms',
                required=False,
                min_value=1,
            )