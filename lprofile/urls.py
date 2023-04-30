from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile1", views.profile1, name="profile1"),
    path("create", views.create, name="create")
]