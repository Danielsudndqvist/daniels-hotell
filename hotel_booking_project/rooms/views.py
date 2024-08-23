from django.shortcuts import render, redirect
from .models import Room
from .forms import BookRoomForm

# Create your views here.

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/list.html', {'rooms': rooms})

def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == "POST":
        form = BookRoomForm(request.POST)
        if form.is_valid():
            # Process the booking here
            return redirect('success_page')
    else:
        form = BookRoomForm()
    return render(request, 'rooms/book.html', {'form': form})
