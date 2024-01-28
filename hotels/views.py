from django.views.generic import TemplateView


class IndexTemplateView(TemplateView):
    template_name = 'hotels/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hotel CRM - Home'
        return context
