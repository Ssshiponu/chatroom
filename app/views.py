from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Room, Topic, Msg
from .form import RoomForm


def index(requests):
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
    msgs = room.msg_set.all().order_by('created')
    members = room.members.all()

    if requests.method == "POST":
        Msg.objects.create(
            user=requests.user,
            room=room,
            text=requests.POST.get('msg')
        )
        room.members.add(requests.user)
        return redirect('room', room_id=room.id)
    
    return render(requests, 'room.html', {"room": room, "msgs": msgs, "members": members})

@login_required(login_url='login')
def create_room(requests):
    if requests.method == "POST":
        form = RoomForm(requests.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = requests.user
            room.save()
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
    if room.host == requests.user:
        room.delete()
        messages.success(requests, "Room deleted")
        return redirect('rooms')
    
    messages.error(requests, "You can't delete this room")
    return redirect('rooms')

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
    messages.warning(requests, "Logout successfully ")
    return redirect('index')

def sign_up(requests):
    if requests.method == "POST":
        form = UserCreationForm(requests.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(requests, f'Account created for {username}')
            user.save()
            login(requests, user)
            return redirect('rooms')
    
    form = UserCreationForm()
    return render(requests, 'signup.html', {"form": form})

def del_msg(requests, msg_id):
    msg = Msg.objects.get(id=msg_id)
    if requests.user != msg.user:
        messages.error(requests, "You can't delete this message")
        return redirect('room', room_id=msg.room.id)
    msg.delete()
    messages.success(requests, f"Message deleted")
    return redirect('room', room_id=msg.room.id)