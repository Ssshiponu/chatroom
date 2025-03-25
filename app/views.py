from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Room, Topic
from .form import RoomForm

# Create your views here.
def index(requests):
    messages.success(requests, "Hello")
    return render(requests, 'index.html')

@login_required(login_url='login')
def rooms(requests):
    q = requests.GET.get('q', '')
    rooms = Room.objects.filter(Q(topic__name__contains=q) |
                                Q(name__contains=q) |
                                Q(description__contains=q)
                                )
    room_count = rooms.count()
    topics = Topic.objects.all()
    return render(requests, 'rooms.html', {"rooms": rooms, "topics": topics, "room_count": room_count})

@login_required(login_url='login')
def room(requests, room_id):
    room = Room.objects.get(id=room_id)
    return render(requests, 'room.html', {"room": room})
@login_required(login_url='login')
def create_room(requests):
    if requests.method == "POST":
        form = RoomForm(requests.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')
    return render(requests, 'create_room.html', {"form": RoomForm()})

@login_required(login_url='login')
def edit_room(requests, room_id):
    room = Room.objects.get(id=room_id)
    if requests.method == "POST":
        form = RoomForm(requests.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('rooms')

    return render(requests, 'create_room.html', {"form": RoomForm(instance=room)})

@login_required(login_url='login')
def del_room(requests, room_id):
    room = Room.objects.get(id=room_id)
    if requests.method == "POST":
        room.delete()
        return redirect('rooms')
        
    return render(requests, 'del.html', {"obj":room})

def log_in(requests):
    if requests.method == "POST":
        username = requests.POST.get('username')
        password = requests.POST.get('password')
        next: str = requests.POST.get('next')
        try:
            user = User.objects.get(username=username)
            user = authenticate(requests, username=username, password=password)
            if user is not None:
                login(requests, user)
                messages.success(requests, 'Login successful')
                return redirect('rooms')
            else:
                messages.error(requests, 'incorrect password')
        except:
            messages.error(requests, 'User does not exist')
            
        
    return render(requests, 'auth.html')

@login_required(login_url='login')
def log_out(requests):
    logout(requests)
    return redirect('index')