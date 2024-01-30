from django.http import HttpRequest

from .forms import HotelForm
from .models import Hotel, HotelRoomsCount, Room, RoomType


def save_hotel(request: HttpRequest, form: HotelForm) -> Hotel:
    hotel = form.save(commit=False)
    hotel.owner = request.user
    hotel.save()
    form.save_m2m()
    return hotel


def get_count_field_name(room_type: RoomType) -> str:
    room_type_name = room_type.name.lower().replace(' ', '_')
    return f'{room_type_name}_count'


def create_hotel_rooms_count(hotel: Hotel, form: HotelForm) -> None:
    for room_type in RoomType.objects.all():
        count_field_name = get_count_field_name(room_type=room_type)
        room_count = form.cleaned_data.get(count_field_name, 0)
        room_count = room_count if room_count is not None else 0
        HotelRoomsCount.objects.create(hotel=hotel, room_type=room_type, count=room_count)


def create_rooms_for_hotel(hotel: Hotel) -> None:
    counter = 1
    for room_type in hotel.hotelroomscount_set.exclude(count=0):
        for _ in range(room_type.count):
            Room.objects.create(
                number=counter,
                hotel=hotel,
                type=room_type.room_type,
            )
            counter += 1
