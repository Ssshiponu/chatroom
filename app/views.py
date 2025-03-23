from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Room, Topic
from .form import RoomForm

# Create your views here.
def index(requests):
    return render(requests, 'index.html')

def rooms(requests):
    q = requests.GET.get('q', '')
    rooms = Room.objects.filter(Q(topic__name__contains=q) |
                                Q(name__contains=q) |
                                Q(description__contains=q)
                                )
    room_count = rooms.count()
    topics = Topic.objects.all()
    return render(requests, 'rooms.html', {"rooms": rooms, "topics": topics, "room_count": room_count})

def room(requests, room_id):
    room = Room.objects.get(id=room_id)
    return render(requests, 'room.html', {"room": room})

def create_room(requests):
    if requests.method == "POST":
        form = RoomForm(requests.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')
    return render(requests, 'create_room.html', {"form": RoomForm()})

def edit_room(requests, room_id):
    room = Room.objects.get(id=room_id)
    if requests.method == "POST":
        form = RoomForm(requests.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms')

    return render(requests, 'create_room.html', {"form": RoomForm(instance=room)})

def del_room(requests, room_id):
    room = Room.objects.get(id=room_id)
    if requests.method == "POST":
        room.delete()
        return redirect('rooms')
        
    return render(requests, 'del.html', {"obj":room})