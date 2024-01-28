from django.contrib import admin

from .models import HotelType, Hotel, RoomType, Room, Amenities, HotelAmenities, HotelRoomsCount


@admin.register(HotelType)
class HotelTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    pass


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Room)
class RootAdmin(admin.ModelAdmin):
    pass


@admin.register(Amenities)
class AmenitiesAdmin(admin.ModelAdmin):
    pass


@admin.register(HotelAmenities)
class HotelAmenitiesAdmin(admin.ModelAdmin):
    pass


@admin.register(HotelRoomsCount)
class HotelRoomsCountAdmin(admin.ModelAdmin):
    pass
