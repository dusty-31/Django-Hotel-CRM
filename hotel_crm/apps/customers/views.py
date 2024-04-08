from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import CustomerForm
from .models import Customer


class CustomerCreateView(LoginRequiredMixin, CreateView):
    form_class = CustomerForm
    template_name = 'customers/form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('booking:create') + f'?customer={self.object.pk}'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Create Customer'
        context['submit_value'] = 'Create'
        return context

    def form_valid(self, form: CustomerForm):
        form.instance.created_by = self.request.user

        return super().form_valid(form)


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/form.html'

    def get_success_url(self) -> str:
        return reverse_lazy('customers:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hotel CRM - Update {self.object.first_name} {self.object.last_name}'
        context['submit_value'] = 'Update'
        return context


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = Customer
    template_name = 'customers/customer.html'
    context_object_name = 'customer'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = f'Hotel CRM - {self.object.first_name} {self.object.last_name}'
        return context


class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    template_name = 'customers/list.html'
    context_object_name = 'customers'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Customers List'
        return context

    def get_queryset(self) -> QuerySet[Customer]:
        return Customer.objects.filter(created_by=self.request.user)
