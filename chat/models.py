from django.db import models
from account.models import User

class Chat(models.Model):
    initiator = models.ForeignKey(User,on_delete = models.CASCADE)
    reactor = models.ForeignKey(User,on_delete = models.CASCADE,related_name="reactoe")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created_at', '-updated_at')

    def __str__(self):
        return self.initiator.username

class Message(models.Model):
   chat = models.ForeignKey(Chat,on_delete = models.CASCADE)
   sender = models.ForeignKey(User,on_delete = models.CASCADE)
   receiver = models.ForeignKey(User,on_delete = models.CASCADE,related_name="receiver")
   body = models.TextField(max_length=1000)
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   
   class Meta:
        ordering = ('created_at', 'updated_at')
   def __str__(self):
        return self.sender.username