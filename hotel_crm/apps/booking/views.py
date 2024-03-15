from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, View

from hotel_crm.apps.customers.models import Customer
from hotel_crm.apps.hotels.models import Hotel, Room

from .forms import BookingForm, BookingWithCustomerForm
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


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/list.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Booking List'
        return context


class BookingWithCustomerView(View):
    def get(self, request, *args, **kwargs):
        hotel_id = request.GET.get('hotel_id')
        form = BookingWithCustomerForm()

        if hotel_id:
            rooms = Room.objects.filter(hotel_id=hotel_id, is_available=True).prefetch_related('hotel', 'type')
            data = {'rooms': {room.id: str(room) for room in rooms}}
            return JsonResponse(data)
        else:
            form.fields['room'].queryset = Room.objects.none()
        context = {
            'title': 'Hotel CRM - Create Booking with Customer',
            'form': form,
        }
        return render(request=request, template_name='booking/with_customer_form.html', context=context)

    def post(self, request, *args, **kwargs):
        form = BookingWithCustomerForm(request.POST)
        if form.is_valid():
            customer = Customer.objects.create(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone_number=form.cleaned_data['phone_number'],
                gender=form.cleaned_data['gender'],
                passport_number=form.cleaned_data['passport_number'],
                disability=form.cleaned_data['disability'],
                created_by=request.user,
            )
            Booking.objects.create(
                hotel=form.cleaned_data['hotel'],
                customer=customer,
                room=form.cleaned_data['room'],
                check_in=form.cleaned_data['check_in'],
                check_out=form.cleaned_data['check_out'],
                number_of_guests=form.cleaned_data['number_of_guests'],
                created_by=request.user,
            )
            room_id = form.cleaned_data['room'].id
            room = Room.objects.get(id=room_id)
            change_status_room(room=room, status=False)
            change_status_customer(customer=customer, status=True)
        return redirect('booking:list')
