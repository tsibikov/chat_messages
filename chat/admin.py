from django.contrib import admin
from .models import Chat_message, Messenger_message, Block


class Chat_messageAdmin(admin.ModelAdmin):
    list_display = ("pk","author", "text", "timestamp") 
    search_fields = ("text",) 
    list_filter = ("timestamp",) 
    empty_value_display = "-пусто-" 


class Messenger_messageAdmin(admin.ModelAdmin):
    list_display = ("pk","author", "companion", "text", "timestamp") 
    search_fields = ("text",) 
    list_filter = ("timestamp",) 
    empty_value_display = "-пусто-" 

class  BlockAdmin(admin.ModelAdmin):
    list_display = ("pk", "chat_user")
    empty_value_display = "-пусто-" 


admin.site.register(Block, BlockAdmin)   
admin.site.register(Chat_message, Chat_messageAdmin) 
admin.site.register(Messenger_message, Messenger_messageAdmin)    