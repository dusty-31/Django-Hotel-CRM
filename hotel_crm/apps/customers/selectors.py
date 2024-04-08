import datetime
from typing import Optional

from django.db.models import Q, QuerySet
from django.utils import timezone

from hotel_crm.apps.booking.models import Booking


def get_customer_bookings_by_dates(
    customer_id: int,
    check_in: Optional[datetime.date] = None,
    check_out: Optional[datetime.date] = None,
) -> QuerySet[Booking]:
    q = Q(customer_id=customer_id, is_active=True)
    if check_in is not None:
        q &= Q(check_out__gte=check_in)
    if check_out is not None:
        q &= Q(check_in__lte=check_out)
    print(Booking.objects.filter(q).query)
    return Booking.objects.filter(q)


def get_current_customer_bookings(customer_id: int) -> QuerySet[Booking]:
    now_date = timezone.now().date()
    return get_customer_bookings_by_dates(customer_id=customer_id, check_in=now_date, check_out=now_date)


def get_future_customer_bookings(customer_id: int) -> QuerySet[Booking]:
    now_date = timezone.now().date()
    return get_customer_bookings_by_dates(customer_id=customer_id, check_in=now_date)
