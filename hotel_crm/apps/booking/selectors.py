from django.db.models import Q

from hotel_crm.apps.hotels.models import Hotel, Room

from .models import Booking


def get_available_rooms_by_hotel_id(hotel_id=None, order_by: list = None):
    if hotel_id is None:
        return Room.objects.none()

    queryset = Room.objects.filter(hotel_id=hotel_id).prefetch_related('hotel', 'type')

    if order_by:
        queryset = queryset.order_by(*order_by)
    return queryset


def get_available_rooms_by_number_of_guests(hotel_id, number_of_guests=None, order_by: list = None):
    if number_of_guests is None:
        return Room.objects.none()

    queryset = Room.objects.filter(hotel_id=hotel_id, type__max_occupancy__gte=number_of_guests).prefetch_related(
        'hotel', 'type'
    )

    if order_by:
        queryset = queryset.order_by(*order_by)
    return queryset


def get_available_rooms(hotel_id=None, number_of_guests=None, order_by: list = None):
    if hotel_id is None and number_of_guests is None:
        return Room.objects.none()

    queryset = get_available_rooms_by_hotel_id(hotel_id=hotel_id, order_by=order_by)
    if number_of_guests:
        queryset = get_available_rooms_by_number_of_guests(hotel_id=hotel_id, number_of_guests=number_of_guests)

    if order_by:
        queryset = queryset.order_by(*order_by)
    return queryset


def get_available_hotels_by_dates(owner, check_in=None, check_out=None, order_by: list = None):
    if check_in is None or check_out is None:
        return Hotel.objects.none()

    booked_hotel_ids = Booking.objects.filter(
        Q(check_in__lte=check_out) & Q(check_out__gte=check_in) & Q(is_active=True)
    ).values_list('room__hotel_id', flat=True)

    queryset = Hotel.objects.filter(owner=owner).exclude(id__in=booked_hotel_ids).distinct()

    if order_by:
        queryset = queryset.order_by(*order_by)
    return queryset
