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
    path("connections", views.conn, name="connections"),
    path("delete/<str:des>",views.deletepost, name="delete")
]