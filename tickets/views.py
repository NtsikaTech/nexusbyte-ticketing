from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django_ratelimit.decorators import ratelimit
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Ticket
from .forms import TicketForm

# Custom admin check
def admin_required(user):
    return user.is_staff

# Home page view
def home(request):
    return HttpResponse("Welcome to the homepage!")

# Create Ticket view (Using the form)
@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
        else:
            return HttpResponse("Invalid data", status=400)
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

# Delete Ticket view (Admin only)
@login_required
@user_passes_test(admin_required)
def delete_ticket(request, ticket_id):
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return HttpResponse("Ticket not found", status=404)

    if ticket.owner != request.user:
        return HttpResponseForbidden("You cannot delete this ticket")

    ticket.delete()
    return HttpResponse("Ticket deleted successfully")

# API View for tickets
class TicketViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.all()
        return Response({'tickets': tickets})

# Rate-limited Ticket creation view
@ratelimit(key='ip', rate='5/m', method='ALL')
def create_ticket_rate_limited(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        ticket = Ticket(title=title, description=description)
        ticket.save()
        return HttpResponse("Ticket created successfully!")
    return render(request, 'tickets/create_ticket.html')

# View to list all tickets
def ticket_list(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

# View to display a single ticket
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket})

# Ticket Create View using a form
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})
