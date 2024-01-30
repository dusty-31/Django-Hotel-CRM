from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, TemplateView, UpdateView

from .forms import HotelForm
from .models import Hotel
from .services import create_hotel_rooms_count, create_rooms_for_hotel, save_hotel


class IndexTemplateView(TemplateView):
    template_name = 'hotels/index.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Home'
        return context


class HotelCreateView(View):
    template_name = 'hotels/form.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        context = {
            'title': 'Hotel CRM - Create Hotel',
            'form': HotelForm(),
            'submit_value': 'Create',
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = save_hotel(request=request, form=form)
            create_hotel_rooms_count(hotel=hotel, form=form)
            create_rooms_for_hotel(hotel=hotel)
            return redirect(reverse_lazy('hotels:detail', kwargs={'pk': hotel.pk}))

        context = {
            'title': 'Hotel CRM - Create Hotel',
            'form': form,
        }
        return render(request=request, template_name=self.template_name, context=context)


class HotelDetailView(DetailView):
    model = Hotel
    template_name = 'hotels/hotel.html'
    context_object_name = 'hotel'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hotel CRM - {self.object.name}'
        return context


class HotelUpdateView(UpdateView):
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
