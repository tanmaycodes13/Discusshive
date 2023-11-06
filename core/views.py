from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, forms
from django.contrib import messages
from core.models import Room, Messages, Topic
from core.forms import RoomForm


def login_user(request):
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("Username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User is not registered")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or Password not correct")
    return render(request, "core/login_register.html", context={"page": page})


def login_register(request):
    user_form = forms.UserCreationForm()
    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Error occured in user registration")
    return render(request, "core/login_register.html", context={"form": user_form})


def logout_user(request):
    logout(request)
    return redirect("home")


def home(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    room_count = get_count(rooms)
    topics = Topic.objects.all()
    return render(
        request,
        "core/home.html",
        context={"rooms": rooms, "topics": topics, "room_count": room_count},
    )


def get_count(instance):
    return instance.count()


def room(request, pk):
    room_context = None
    room_context = Room.objects.get(id=pk)
    return render(request, "core/room.html", context={"rooms": room_context})


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "core/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Hey why are you Trespassing!!!")
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "core/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Hey why are you Trespassing!!!")
    if request.method == "POST":
        room.delete()
        return redirect("home")
    return render(request, "core/delete.html", {"obj": room})
