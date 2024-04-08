from django.views.generic import ListView

from hotel_crm.apps.customers.models import Customer


class ContactListView(ListView):
    model = Customer
    template_name = 'contacts/list.html'
    context_object_name = 'contacts'

    def get_queryset(self, *args, **kwargs):
        return Customer.objects.filter(created_by=self.request.user)
