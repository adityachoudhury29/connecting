from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class posts(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    desc=models.CharField(max_length=1000)
    time=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='likes')
    dislikes=models.ManyToManyField(User,related_name='dislikes')
    postimg=models.ImageField(null=True,blank=True,upload_to="media/postimages")
    def number_of_likes(self):
        return self.likes.count()
    def number_of_dislikes(self):
        return self.dislikes.count()
    def __str__(self):
        return self.desc

class profile1(models.Model):
    profowner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="profowner")
    profimg=models.ImageField(null=True,blank=True,upload_to="media/profimages")
    about=models.CharField(max_length=300,blank=True)
    follower=models.ManyToManyField(User,related_name="follower",blank=True)
    followers=models.ManyToManyField(User,related_name="followers",blank=True)
    connections=models.ManyToManyField(User,related_name="connections",blank=True)
    requests=models.ManyToManyField(User,related_name="requests",blank=True)
    def number_of_conns(self):
        return self.follower.count()
    def number_of_followers(self):
        return self.followers.count()
    def number_of_connections(self):
        return self.connections.count()
    def __str__(self):
        return f'{self.profowner.first_name} {self.profowner.last_name}'
    
class comments(models.Model):
    comment_owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,related_name='c_owner')
    c_post=models.ForeignKey(posts,on_delete=models.CASCADE,blank=True,null=True,related_name='c_post')
    message=models.CharField(max_length=300)
    def __str__(self):
        return f'{self.comment_owner}:{self.c_post}'