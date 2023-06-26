from django.db import models
from lprofile.models import User

class messages(models.Model):
    sender=models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE,blank=True)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}'
    
    def last_10_messages(self):
        return messages.objects.order_by('-timestamp').all()[:10]