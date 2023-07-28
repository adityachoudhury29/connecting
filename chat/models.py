from django.db import models
from lprofile.models import User

class room(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class messages(models.Model):
    roomname = models.ForeignKey(room,on_delete=models.CASCADE,related_name='roomname')
    sender=models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE,blank=True)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    file=models.FileField(null=True,blank=True,upload_to="media/chatfiles")

    def __str__(self):
        return f'{self.sender.username}:{self.timestamp}'
    
    def strtime(self):
        return self.timestamp.strftime("%B %d, %Y, %H:%M")
