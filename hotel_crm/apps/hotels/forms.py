from django import forms

from .models import Amenities, Hotel, HotelType, Room, RoomType


class HotelForm(forms.ModelForm):
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

        [self.add_room_type_count_field(room_type=room_type) for room_type in RoomType.objects.all()]

    def add_room_type_count_field(self, room_type: RoomType) -> None:
        room_type_name = room_type.name.lower().replace(' ', '_')
        count_field_name = f'{room_type_name}_count'
        self.fields[count_field_name] = forms.IntegerField(
            label=f'Number of {room_type.name} rooms',
            required=False,
            min_value=1,
        )


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = (
            'number',
            'type',
            'is_available',
        )
