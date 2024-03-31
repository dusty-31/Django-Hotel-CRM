from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, DetailView, ListView, TemplateView

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
        form_class = self.get_form_class()
        user = self.request.user
        hotel_id = self.request.GET.get('hotel_id')
        customer_id = self.request.GET.get('customer')
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        number_of_guests = self.request.GET.get('number_of_guests')
        form = form_class(
            hotel_id=hotel_id,
            created_by=user,
            customer_id=customer_id,
            check_in=check_in,
            check_out=check_out,
            number_of_guests=number_of_guests,
            **self.get_form_kwargs(),
        )
        return form

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: BookingForm):
        response = super().form_valid(form)
        room = form.cleaned_data['room']
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


class BookingDeleteView(TemplateView):
    template_name = 'booking/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Delete Booking'
        return context

    def get(self, request, *args, **kwargs):
        booking = get_object_or_404(klass=Booking, pk=kwargs['pk'])
        context = self.get_context_data()
        context['booking'] = booking
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        booking = get_object_or_404(Booking, pk=kwargs['pk'])
        room = booking.room
        change_status_room(room=room, status=True)
        customer = booking.customer
        change_status_customer(customer=customer, status=False)
        booking.is_active = False
        booking.save()
        return redirect(to='booking:detail', pk=booking.pk)


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
