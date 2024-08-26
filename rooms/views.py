from django.shortcuts import render, redirect
from .models import Room
from django.views.generic.base import TemplateView



def get_base(request):
    return render(request, 'base.html',)

def room_list(request):
    return render(request, 'list.html',)

def book_room(request,):
    return render(request, 'book.html',)
    
def submit_booking(request):
    return render(request, 'booking_confirmation.html')