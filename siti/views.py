from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

from app.models import *

def home(request):
    maps = Maps.objects.all()
    crud = Crud.objects.all()

    return render(request, 'index.html', context = {
        "maps": maps,
        "crud" : crud
    })

def maps(request):
    maps = Maps.objects.all()
    if request.method == "POST":
        Maps.objects.create(
            kode = request.POST.get("kode"),
            lokasi = request.POST.get("lokasi")
        )

    if request.user.is_authenticated:
        return render(request, "maps.html", context = {
            "maps": maps,
        })
    else:
        return redirect("/login")

def mapsUpdate(request, id):
    maps = Maps.objects.all()
    map_id = Maps.objects.get(id = id)

    if request.method == "POST":
        map_id.kode = request.POST.get("kode")
        map_id.lokasi = request.POST.get("lokasi")
        map_id.save()

    if request.user.is_authenticated:
        return render(request, "maps.html", context = {
            "maps": maps,
            "map_id" : map_id
        })
    else:
        return redirect("/login")


def mapsDelete(request, id):
    if request.user.is_authenticated:
        map_id = Maps.objects.get(id = id)
        map_id.delete()
        return redirect("/maps")
    else:
        return redirect("/login")


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        user = authenticate(request, username = request.POST.get("username"), password = request.POST.get("password"))
        if user is not None:
            auth_login(request, user)
            return redirect("/")

    return render(request, 'login.html')

def table(request):
    gramedias = Crud.objects.all()
    if request.method == "POST":
        Crud.objects.create(
            nama = request.POST.get("nama"),
            lokasi = request.POST.get('alamat'),
            keterangan = request.POST.get("keterangan")
        )
    
    if request.user.is_authenticated:
        return render(request, "table.html", context= {
            "grammedias" : gramedias,
        })
    else:
        return redirect("/login")


def tableUpdate(request, id):
    gramedias = Crud.objects.all()
    gramedia_id = Crud.objects.get(id=id)
    if request.method == "POST":
        gramedia_id.nama = request.POST.get("nama")
        gramedia_id.lokasi = request.POST.get('alamat')
        gramedia_id.keterangan = request.POST.get("keterangan")
        gramedia_id.save()
        return redirect("/table")

    if request.user.is_authenticated:
        return render(request, "table.html", context= {
            "grammedias" : gramedias,
            "gramedia_id" : gramedia_id
        })
    else:
        return redirect("/login")
        

def tableDelete(request, id):
    if request.user.is_authenticated:
        gramedia_id = Crud.objects.get(id = id)
        gramedia_id.delete()
        return redirect("/table")
    else:
        return redirect("/table")


def register(request):
    if request.method == "POST":
        u = User.objects.create(
            username = request.POST.get("username")
        )
        u.set_password( request.POST.get("password"))
        u.is_staff = True
        u.is_superuser = True
        u.save()
        return redirect("/")
    return render(request, 'register.html')

def keluar(request):
    logout(request)
    return redirect("/")
