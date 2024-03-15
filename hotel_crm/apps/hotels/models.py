from django.db import models
from django.urls import reverse

from hotel_crm.apps.users.models import User


class Amenities(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'


class HotelType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    count_of_stars = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    hotel_type = models.ForeignKey(HotelType, on_delete=models.PROTECT)
    amenities = models.ManyToManyField(
        to=Amenities,
        through='HotelAmenities',
        through_fields=('hotel', 'amenity'),
        related_name='hotels',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'

    @property
    def total_rooms(self):
        return self.room_set.count()

    @property
    def free_rooms(self):
        return self.room_set.filter(is_available=True).count()

    @property
    def populated_rooms(self):
        return self.room_set.filter(is_available=False).count()

    def get_absolute_url(self):
        return reverse(viewname='hotels:detail', kwargs={'pk': self.pk})


class HotelAmenities(models.Model):
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE)
    amenity = models.ForeignKey(to=Amenities, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.hotel.name} - {self.amenity.name}'


class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_occupancy = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Room(models.Model):
    number = models.IntegerField()
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE)
    type = models.ForeignKey(to=RoomType, on_delete=models.PROTECT)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'Hotel: {self.hotel.name} - Number {self.number} - Type: {self.type.name}'

    def get_absolute_url(self):
        return reverse(viewname='hotels:room_detail', kwargs={'pk': self.pk})

    @property
    def active_booking(self):
        return self.booking_set.filter(is_active=True).first()


class HotelRoomsCount(models.Model):
    hotel = models.ForeignKey(to=Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(to=RoomType, on_delete=models.PROTECT)
    count = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.hotel.name} - {self.room_type.name} - {self.count} rooms'

    class Meta:
        verbose_name = 'Hotel Rooms Count'
        verbose_name_plural = 'Hotel Rooms Count'
