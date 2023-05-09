from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profilefunc/<str:uname>", views.profilefunc, name="profile1"),
    path("create", views.create, name="create"),
    path("like/<int:pk>", views.like, name="like"),
    path("dislike/<int:pk>", views.dislike, name="dislike"),
    path("followings/<str:uname>", views.foll, name="followings"),
    path("delete/<int:id>",views.deletepost, name="delete"),
    path("addconnection",views.addc, name="addc"),
    path("follow/<str:uname>",views.add, name="follow"),
    path("unfollow/<str:uname>",views.remove, name="unfollow"),
    path("edit",views.editprof, name="edit"),
]