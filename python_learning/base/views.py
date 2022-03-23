from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Room, Topic
from .forms import RoomForm


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

    try:
        user = User.objects.get(username=username)
    except:
        pass

    context = {}
    return render(request, "login_register.html", context)


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q))

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"room": room}
    return render(request, "room.html", context)


def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "room_form.html", context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}

    return render(request, "room_form.html", context)


def delete_room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == "POST":
        room.delete()
        return redirect("home")

    return render(request, "delete.html", {"obj": room})