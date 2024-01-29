from django.urls import path

from . import views

app_name = 'hotels'

urlpatterns = [
    path('create/', views.HotelCreateView.as_view(), name='create'),
    path('<int:pk>/', views.HotelDetailView.as_view(), name='detail'),
]
