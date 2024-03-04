from django.urls import path

from . import views

app_name = 'customer'

urlpatterns = [
    path('create/', views.BookingCreateView.as_view(), name='create'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.BookingDeleteView.as_view(), name='delete'),
]
