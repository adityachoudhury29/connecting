from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, posts, profile1, comments, jobs
# Create your views here.

def login_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
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
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
 
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "lprofile/register.html", {
                "message": "Passwords must match!"
            })

        try:
            if username is "":
                return render(request, "lprofile/register.html",{
                    "message": "Username cannot be empty!"
                })
            user = User.objects.create_user(username, email, password)
            user.first_name=first_name
            user.last_name=last_name
            l=[user.first_name,user.last_name,user.password]
            for i in l:
                if i is "":
                    return render(request, "lprofile/register.html",{
                        "message": "All non-optional fields are compulsory!"
                    })
                else:
                    continue
            user.save()
        except IntegrityError:
            return render(request, "lprofile/register.html", {
                "message": "Username already taken!"
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
        img=request.FILES.get("postpic",False)
        user=request.user
        if desc is "":
            return render(request,'lprofile/create.html',{
                'message':'Post cannot be empty!'
            })
        if img != False:
            newpost=posts(owner=user,desc=desc,postimg=img)
        else:
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
        try:
            myprof=profile1.objects.get(profowner=user)
            return render(request,'lprofile/profile1.html',{
                'myprof':myprof,
                'mypost':posts.objects.filter(owner=user)
            })
        except ObjectDoesNotExist:
            myprof=profile1(profowner=user)
            myprof.save()
            return render(request,'lprofile/profile1.html',{
                'myprof':myprof
            })
    except ObjectDoesNotExist:
        return render(request,'lprofile/profnotfound.html')
    
def foll(request,uname):
    try:
        user=User.objects.get(username=uname)
        conn=profile1.objects.get(profowner=user)
        conns=conn.follower.all()
        folls=conn.followers.all()
        connections=conn.connections.all()
        return render(request,'lprofile/conn.html',{
            'conns':conns,
            'conn':conn,
            'folls':folls,
            'connections':connections
        })
    except ObjectDoesNotExist:
        return render(request,'lprofile/noconn.html')

def deletepost(request,id):
    post=posts.objects.get(pk=id)
    if post.owner==request.user:
        post.delete()
        return HttpResponseRedirect(reverse('profile1',args=[request.user]))

def addc(request):
    me=profile1.objects.get(profowner=request.user)
    profiles=profile1.objects.all().exclude(profowner=request.user)
    return render(request,'lprofile/addc.html',{
        'users':profiles,
        'me':me.follower.all(),
        'mec':me.connections.all(),
        'mer':me.requests.all()
    })

def add(request,uname):
    user=User.objects.get(username=uname)
    profile=profile1.objects.get(profowner=request.user)
    if request.method=='POST':
        if user not in profile.follower.all():
            profile.follower.add(user)
            profile1.objects.get(profowner=user).followers.add(request.user)
        return HttpResponseRedirect(reverse('followings',args=[request.user]))

def remove(request,uname):
    user=User.objects.get(username=uname)
    profile=profile1.objects.get(profowner=request.user)
    if request.method=='POST':
        if user in profile.follower.all():
            profile.follower.remove(user)
            profile1.objects.get(profowner=user).followers.remove(request.user)
        return HttpResponseRedirect(reverse('followings',args=[request.user]))
    
def editprof(request):
    myprof=profile1.objects.get(profowner=request.user)
    if request.method=='GET':
        return render(request,'lprofile/editprof.html',{
            'myprof':myprof
        })
    else:
        fn=request.POST["firstname"]
        ln=request.POST["lastname"]
        role=request.POST["role"]
        abt=request.POST["about"]
        pic=(request.FILES['pic'] if 'pic' in request.FILES else False)
        if pic==False:
            myprof.profimg=''
        else:
            myprof.profimg=pic
        myprof.profowner.first_name=fn
        myprof.profowner.last_name=ln
        myprof.role=role
        myprof.about=abt
        myprof.save()
        return HttpResponseRedirect(reverse('profile1',args=[request.user]))
    
def connect(request,uname):
    user=User.objects.get(username=uname)
    profile=profile1.objects.get(profowner=user)
    if request.method=='POST':
        if request.user not in profile.requests.all():
            profile.requests.add(request.user)
        return HttpResponseRedirect(reverse('addc'))

def disconnect(request,uname):
    user=User.objects.get(username=uname)
    profile=profile1.objects.get(profowner=request.user)
    userprof=profile1.objects.get(profowner=user)
    if request.method=='POST':
        if user in profile.connections.all():
            profile.connections.remove(user)
            userprof.connections.remove(request.user)
        return HttpResponseRedirect(reverse('addc'))

def accept(request,uname):
    user=User.objects.get(username=uname)
    uprof=profile1.objects.get(profowner=user)
    profile=profile1.objects.get(profowner=request.user)
    if request.method=='POST':
        profile.requests.remove(user)
        profile.connections.add(user)
        uprof.connections.add(request.user)
    return HttpResponseRedirect(reverse('addc'))

def decline(request,uname):
    user=User.objects.get(username=uname)
    profile=profile1.objects.get(profowner=request.user)
    if request.method=='POST':
        profile.requests.remove(user)
    return HttpResponseRedirect(reverse('addc'))

def gotocomments(request,id):
    post=posts.objects.get(pk=id)
    if request.method=='GET':
        comms=comments.objects.filter(c_post=post)
        return render(request,'lprofile/comments.html',{
            'post':post,
            'comms':comms
        })
    else:
        c_owner=request.user
        message=request.POST["message"]
        comm=comments(comment_owner=c_owner,message=message,c_post=post)
        comm.save()
        comms=comments.objects.filter(c_post=post)
        return render(request,'lprofile/comments.html',{
            'post':post,
            'comms':comms
        })

def job(request):
    joblistings=jobs.objects.all()
    return render(request,'lprofile/jobs.html',{
        'joblistings':joblistings,
    })

def jobpost(request):
    if request.method=='GET':
        return render(request,'lprofile/jobpost.html')
    elif request.method=='POST':
        title=request.POST["j_title"]
        company=request.POST["company"]
        desc=request.POST["j_desc"]
        job=jobs(j_provider=request.user,j_title=title,company=company,j_desc=desc)
        job.save()
        return HttpResponseRedirect(reverse('job'))

def apply(request,id):
    job=jobs.objects.get(pk=id)
    if request.method=='POST':
        job.applicants.add(request.user)
        return HttpResponseRedirect(reverse('job'))

def applicants(request,id):
    job=jobs.objects.get(pk=id)
    applics=job.applicants.all()
    if request.method=='POST':
        return render(request,'lprofile/applicants.html',{
            'applics':applics
        })