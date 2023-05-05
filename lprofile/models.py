from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class posts(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="user")
    desc=models.CharField(max_length=1000)
    time=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='likes')
    dislikes=models.ManyToManyField(User,related_name='dislikes')
    def number_of_likes(self):
        return self.likes.count()
    def number_of_dislikes(self):
        return self.dislikes.count()
    def __str__(self):
        return self.desc

class profile1(models.Model):
    profowner=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name="profowner")
    about=models.CharField(max_length=300,blank=True)
    connection=models.ManyToManyField(User,related_name="connection",blank=True)
    def number_of_conns(self):
        return self.connection.count()
    def __str__(self):
        return f'{self.profowner.first_name} {self.profowner.last_name}'
    