from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.views.generic import CreateView, DetailView

from hotel_crm.apps.hotels.models import Hotel, Room

from .forms import BookingForm
from .models import Booking


class BookingCreateView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'booking/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Create Booking'
        context['submit_value'] = 'Create'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user
        form.fields['customer'].queryset = user.customer_set.all()
        form.fields['hotel'].queryset = Hotel.objects.filter(owner=user).prefetch_related('owner')
        return form

    def get(self, request, *args, **kwargs):
        hotel_id = request.GET.get('hotel_id')
        if hotel_id:
            rooms = Room.objects.filter(hotel_id=hotel_id, is_available=True).prefetch_related('hotel', 'type')
            data = {'rooms': {room.id: str(room) for room in rooms}}
            return JsonResponse(data)
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: BookingForm):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Booking Detail'
        return context
