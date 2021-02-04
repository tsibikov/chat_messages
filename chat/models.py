from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

 
 
class Chat_message(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-timestamp",)


class Messenger_message(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    text = models.TextField()
    timestamp = models.DateTimeField('Дата сообщения', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='author')
    companion = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='companion')
    room_name = models.IntegerField()                          
    
    
    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):   
        return f"{self.timestamp} {self.author} {self.companion} {self.text}"       

class Block(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    chat_user = models.ForeignKey(User, on_delete=models.CASCADE, 
                               related_name='block_user')   
