from hotel_crm.apps.hotels.models import Room


def get_available_rooms_by_hotel_id(hotel_id=None, order_by: list = None):
    if hotel_id is None:
        return Room.objects.none()
    queryset = Room.objects.filter(hotel_id=hotel_id, is_available=True).prefetch_related('hotel', 'type')
    if order_by:
        queryset = queryset.order_by(*order_by)
    return queryset
