from django.views.generic import CreateView, DetailView

from hotel_crm.apps.hotels.models import Hotel, Room

from .forms import BookingForm
from .models import Booking


class BookingCreateView(CreateView):
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
        form.fields['room'].queryset = Room.objects.filter(hotel__owner=user, is_available=True).prefetch_related(
            'hotel', 'type'
        )
        return form

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
