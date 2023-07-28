from django.urls import path
from chat import views
import lprofile

urlpatterns=[
    path("", lprofile.views.chatapp, name="chat"),
    path("<str:room_name>/", views.roomin, name="room"),
]