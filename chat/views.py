from django.shortcuts import render
from lprofile.models import User, profile1
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

@login_required
def chatroom(request):
    return render(request,'chat/chatroom.html',{
        'chatters':User.objects.all().exclude(username=request.user.username)
    })

@login_required
def roomin(request, room_name):
    chatters=User.objects.all().exclude(username=request.user.username)
    try:
        room_1=room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        room_1=room(name=room_name)
        room_1.save()
    chats=[]
    chats=messages.objects.filter(roomname=room_1)
    other_user=User.objects.get(username=(room_name.replace('_chatroomfor_','')).replace(request.user.username,''))
    theirprof=profile1.objects.get(profowner=other_user)
    myprof=profile1.objects.get(profowner=request.user)
    return render(request,"chat/room.html",{
        'room_name': room_name,
        'chats':chats,
        'username':request.user.username,
        'other_user':other_user,
        'theirprof':theirprof,
        'myprof':myprof,
        'chatters':chatters
    })
