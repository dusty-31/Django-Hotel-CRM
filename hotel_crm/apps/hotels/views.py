from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import HotelForm, RoomForm
from .models import Hotel, Room
from .services import create_hotel_rooms_count, create_rooms_for_hotel


class IndexTemplateView(TemplateView):
    template_name = 'hotels/index.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Home'
        return context


class HotelCreateView(LoginRequiredMixin, CreateView):
    form_class = HotelForm
    template_name = 'hotels/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Create Hotel'
        context['submit_value'] = 'Create'
        return context

    def get_success_url(self):
        return reverse_lazy('hotels:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        hotel = self.object
        create_hotel_rooms_count(hotel=hotel, form=form)
        create_rooms_for_hotel(hotel=hotel)
        return response


class HotelDetailView(LoginRequiredMixin, DetailView):
    model = Hotel
    template_name = 'hotels/hotel.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hotel CRM - {self.object.name}'
        context['rooms'] = self.object.room_set.all().order_by('number')
        return context


class HotelUpdateView(LoginRequiredMixin, UpdateView):
    model = Hotel
    template_name = 'hotels/form.html'
    form_class = HotelForm
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hotel CRM - {self.object.name}'
        context['submit_value'] = 'Update'
        return context

    def get_success_url(self) -> str:
        return reverse_lazy('hotels:detail', kwargs={'pk': self.object.pk})

    def get_form(self, form_class=None) -> HotelForm:
        form = super().get_form(form_class)

        for room_type_count in self.object.hotelroomscount_set.all():
            room_type_name = room_type_count.room_type.name.lower().replace(' ', '_')
            count_field_name = f'{room_type_name}_count'

            form.fields[count_field_name].widget.attrs['readonly'] = True
            form.fields[count_field_name].initial = room_type_count.count

        return form

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            raise PermissionDenied('You do not have permission to edit this hotel.')
        return super().dispatch(request, *args, **kwargs)


class HotelDeleteView(LoginRequiredMixin, DeleteView):
    model = Hotel
    template_name = 'hotels/delete.html'
    context_object_name = 'hotel'
    success_url = reverse_lazy('hotels:list')

    def delete(self, request, *args, **kwargs):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied("You are not the owner of this hotel.")
        success_url = self.get_success_url()
        self.get_object().delete()
        return redirect(success_url)


class HotelListView(LoginRequiredMixin, ListView):
    model = Hotel
    template_name = 'hotels/list.html'
    context_object_name = 'hotels'
    paginate_by = 10

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Hotels'
        return context

    def get_queryset(self) -> QuerySet[Hotel]:
        return Hotel.objects.filter(owner=self.request.user)


class RoomDetailView(LoginRequiredMixin, DetailView):
    model = Room
    template_name = 'hotels/room.html'
    context_object_name = 'room'

    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        return context


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'hotels/room_form.html'
    form_class = RoomForm

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hotel CRM - Update Room #{self.object.number}'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs
