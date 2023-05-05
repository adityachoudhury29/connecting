from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, posts, profile1
# Create your views here.

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "lprofile/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "lprofile/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
 
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lprofile/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.first_name=first_name
            user.last_name=last_name
            user.save()
        except IntegrityError:
            return render(request, "lprofile/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "lprofile/register.html")
    
def index(request):
    posts2=posts.objects.all()
    return render(request,'lprofile/index.html',{
        'posts1':posts2
    })

def create(request):
    if request.method=='GET':
        return render(request,'lprofile/create.html')
    else:
        desc=request.POST["desc"]
        user=request.user
        newpost=posts(owner=user,desc=desc)
        newpost.save()
        posts1=posts.objects.all()
        return render(request,'lprofile/index.html',{
            'posts1':posts1
        })

def like(request,pk):
    post=get_object_or_404(posts,id=request.POST.get('id'))
    if request.user in post.dislikes.all():
        post.dislikes.remove(request.user)
        post.likes.add(request.user)
    elif request.user in post.likes.all() and request.user not in post.dislikes.all():
        post.likes.remove(request.user)
    elif request.user not in post.likes.all() and request.user not in post.dislikes.all():
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('index'))

def dislike(request,pk):
    post=get_object_or_404(posts,id=request.POST.get('id'))
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        post.dislikes.add(request.user)
    elif request.user in post.dislikes.all() and request.user not in post.likes.all():
        post.dislikes.remove(request.user)
    elif request.user not in post.likes.all() and request.user not in post.dislikes.all():
        post.dislikes.add(request.user)
    return HttpResponseRedirect(reverse('index'))

def profilefunc(request,uname):  
    try:
        user=User.objects.get(username=uname)
        if profile1.objects.get(profowner=user) is None:
            myprof=profile1(profowner=user)
            myprof.save()
        else:
            myprof=profile1.objects.get(profowner=user)
        return render(request,'lprofile/profile1.html',{
            'myprof':myprof
        })
    except ObjectDoesNotExist:
        return render(request,'lprofile/profnotfound.html')
    
def conn(request):
    try:
        conn=profile1.objects.get(profowner=request.user)
        conns=conn.connection.all()
        return render(request,'lprofile/conn.html',{
            'conns':conns,
            'conn':conn
        })
    except ObjectDoesNotExist:
        return render(request,'lprofile/noconn.html')

def deletepost(request,des):
    post=posts.objects.get(desc=des)
    post.delete()
    return HttpResponseRedirect(reverse('index'))