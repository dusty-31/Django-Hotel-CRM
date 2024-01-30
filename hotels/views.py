from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from django.http import HttpRequest, HttpResponse

from .models import Hotel
from .forms import HotelCreateForm
from .services import create_rooms_for_hotel, save_hotel, create_hotel_rooms_count


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
            'form': HotelCreateForm(),
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        form = HotelCreateForm(request.POST)
        if form.is_valid():
            hotel = save_hotel(request=request, form=form)
            create_hotel_rooms_count(hotel=hotel, form=form)
            create_rooms_for_hotel(hotel=hotel)
            return redirect(reverse_lazy('hotels:index'))

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
