from django.urls import path

from . import views

app_name = 'hotels'

urlpatterns = [
    path('', views.IndexTemplateView.as_view(), name='index'),
]
