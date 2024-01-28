from django.db import models

from users.models import User


class Amenities(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rating = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f'<Amenities: {self.name}>'

    class Meta:
        verbose_name = 'Amenity'
        verbose_name_plural = 'Amenities'


class HotelType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'<HotelType: {self.name}>'


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    count_of_stars = models.PositiveIntegerField(default=0)
    total_rooms = models.PositiveIntegerField(default=0)
    hotel_type = models.ForeignKey(HotelType, on_delete=models.PROTECT)
    amenities = models.ManyToManyField(
        to=Amenities,
        through='HotelAmenities',
        through_fields=('hotel', 'amenity'),
        related_name='hotels',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.OneToOneField(to=User, on_delete=models.PROTECT)

    def __str__(self):
        return f'<Hotel: {self.name}>'

    class Meta:
        verbose_name = 'Hotel'
        verbose_name_plural = 'Hotels'


class HotelAmenities(models.Model):
    hotel = models.ForeignKey(to=Hotel, on_delete=models.PROTECT)
    amenity = models.ForeignKey(to=Amenities, on_delete=models.PROTECT)

    def __str__(self):
        return f'<HotelAmenities: {self.hotel.name} - {self.amenity.name}>'


class RoomType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_occupancy = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'<RoomType: {self.name}>'


class Room(models.Model):
    number = models.IntegerField()
    hotel = models.ForeignKey(to=Hotel, on_delete=models.PROTECT)
    type = models.ForeignKey(to=RoomType, on_delete=models.PROTECT)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'<Room: Number {self.number} - Type: {self.type.name}>'
