from django.shortcuts import render
from lprofile.models import User
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
    try:
        room_1=room.objects.get(name=room_name)
    except ObjectDoesNotExist:
        room(name=room_name).save()
    messages_of_room=messages.objects.filter(roomname=room_1).order_by('-timestamp')
    return render(request,"chat/room.html",{
        'prevmessages':messages_of_room,
        'room_name': room_name,
        'username':request.user.username
    })
