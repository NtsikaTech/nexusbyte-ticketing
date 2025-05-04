from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include('tickets.urls')),  # Include the tickets URLs
]

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('create/', views.ticket_create, name='ticket_create'),
]