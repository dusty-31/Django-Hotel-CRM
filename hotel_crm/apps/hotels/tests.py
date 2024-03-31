from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from .models import Amenities, Hotel, HotelType, RoomType


class IndexTemplateViewTestCase(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('index'))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, template_name='hotels/index.html')

    def test_context(self):
        self.assertEqual(self.response.context['title'], 'Hotel CRM - Home')

    def test_title(self):
        self.assertContains(self.response, '<title>Hotel CRM - Home</title>')


class HotelCreateViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse('hotels:create')
        self.user = get_user_model().objects.create_user(
            username='StudentName',
            password='StudentPassword',
            is_student=True,
        )
        self.client.login(username='StudentName', password='StudentPassword')
        self.hotel_type = HotelType.objects.create(
            name='Hotel Type Test',
            count_of_stars=5,
            description='Description for Hotel Type Test',
        )
        self.amenities = (
            Amenities.objects.create(name='Amenity Test 1', rating=5.17),
            Amenities.objects.create(name='Amenity Test 2', rating=2.16),
            Amenities.objects.create(name='Amenity Test 3', rating=21.32),
        )
        self.room_types = (
            RoomType.objects.create(name='Room Type Test 1', max_occupancy=1, price=100.00),
            RoomType.objects.create(name='Room Type Test 2', max_occupancy=2, price=250.00),
            RoomType.objects.create(name='Room Type Test 3', max_occupancy=3, price=500.00),
        )
        self.hotel = {
            'name': 'Hotel Test',
            'hotel_type': self.hotel_type.id,
            'amenities': [amenity.id for amenity in self.amenities],
            'room_type_test_1_count': 5,
            'room_type_test_2_count': 10,
            'room_type_test_3_count': 15,
        }

    def test_status_code_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='hotels/form.html')

    def test_status_code_POST(self):
        response = self.client.post(self.url, self.hotel)
        self.assertEqual(response.status_code, 302)

    def test_create_hotel(self):
        self.client.post(self.url, self.hotel)
        self.assertTrue(Hotel.objects.exists())

    def test_create_hotel_owner(self):
        self.client.post(self.url, self.hotel)
        hotel = Hotel.objects.first()
        self.assertEqual(hotel.owner, self.user)

    def test_create_hotel_rooms_count(self):
        self.client.post(self.url, self.hotel)
        hotel = Hotel.objects.first()
        self.assertEqual(hotel.hotelroomscount_set.count(), 3)

    def test_create_rooms_for_hotel(self):
        self.client.post(self.url, self.hotel)
        hotel = Hotel.objects.first()
        self.assertEqual(hotel.room_set.count(), 30)
