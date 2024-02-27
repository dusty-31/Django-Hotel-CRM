from django.urls import path

from . import views

app_name = 'hotels'

urlpatterns = [
    path('create/', views.HotelCreateView.as_view(), name='create'),
    path('<int:pk>/', views.HotelDetailView.as_view(), name='detail'),
    path('update/<int:pk>', views.HotelUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', views.HotelDeleteView.as_view(), name='delete'),
    path('list/', views.HotelListView.as_view(), name='list'),
]
