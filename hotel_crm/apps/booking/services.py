from hotel_crm.apps.hotels.models import Room


def change_status_room(room: Room, status: bool) -> None:
    room.is_available = status
    room.save()


def change_status_customer(customer, status: bool) -> None:
    customer.is_inhabited = status
    customer.save()
