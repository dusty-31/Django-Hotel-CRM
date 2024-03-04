from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, View

from hotel_crm.apps.hotels.models import Hotel, Room

from .forms import BookingForm
from .models import Booking
from .services import change_status_customer, change_status_room


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

        if self.request.method == 'POST':
            hotel_id = self.request.POST.get('hotel')
            if hotel_id:
                rooms = Room.objects.filter(hotel_id=hotel_id, is_available=True).prefetch_related('hotel', 'type')
                form.fields['room'].queryset = rooms
        else:
            form.fields['room'].queryset = Room.objects.none()
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
        response = super().form_valid(form)
        room_id = form.cleaned_data['room'].id
        room = Room.objects.get(id=room_id)
        change_status_room(room=room, status=False)
        change_status_customer(customer=form.instance.customer, status=True)
        return response


class BookingDetailView(DetailView):
    model = Booking
    template_name = 'booking/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Booking Detail'
        return context


class BookingDeleteView(View):
    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(klass=Booking, pk=kwargs['pk'])
        context = {
            'title': 'Hotel CRM - Delete Booking',
            'booking': booking,
        }
        return render(request=request, template_name='booking/delete.html', context=context)

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        room = booking.room
        change_status_room(room=room, status=True)
        customer = booking.customer
        change_status_customer(customer=customer, status=False)
        booking.is_active = False
        booking.save()
        return redirect('booking:detail', pk=booking.pk)
