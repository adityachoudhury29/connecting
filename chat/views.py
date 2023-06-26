import json
from django.shortcuts import render
from lprofile.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

# Create your views here.

@login_required
def chatroom(request):
    return render(request,'chat/chatroom.html',{
        'chatters':User.objects.all().exclude(username=request.user.username)
    })

@login_required
def room(request, room_name):
    return render(request, "chat/room.html",{
        "room_name": room_name,
        'username':mark_safe(json.dumps(request.user.username))
    })
