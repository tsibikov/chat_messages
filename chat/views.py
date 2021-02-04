import json
from django.contrib.auth.decorators import login_required, permission_required
from .models import User, Chat_message, Messenger_message, Block
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from .forms import User_search_form
from django.urls import reverse



def index(request):
    """Главная страница"""
    room_name = 'index'
    return render(request, 'index.html', {'room_name': room_name})


@login_required
def chat(request, room_name):
    account = request.user
    no_permission = Block.objects.filter(chat_user=account)
    if no_permission:
        return render(request, 'block.html') 
    return render(request, 'chat.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'account': mark_safe(json.dumps(account.username))
    })

@login_required
def messenger(request, room_name):
    pass

@login_required
def message_index(request):
    if 'companion' in request.GET:
        form = User_search_form(request.GET)
        if form.is_valid():
            username = form.cleaned_data['companion']   
            comp = User.objects.filter(username=username)
            if comp:
                for c in comp:
                    companion = c
                user_name = request.user
                if companion.username == user_name.username:
                    messages.info(request, (f"Зачем писать сообщение самому себе? Поищи другого собеседника"))
                    return render(request, 'message_index.html', {'form':form})
                else:    
                    if companion.id > user_name.id:
                        room_name = int(str(user_name.id) + str(companion.id))
                    else:
                        room_name = int(str(companion.id) + str(user_name.id)) 
                    return render(request, 'room.html', {
                             'room_name_json': mark_safe(json.dumps(room_name)),
                             'account': mark_safe(json.dumps(user_name.username)),
                             'companion': mark_safe(json.dumps(companion.username))
                    })


  
            else:
                messages.info(request, (f"Пользователь {username} не зарегистрирован на сайте"))         
    else:
        form = User_search_form()       
    return render(request, 'message_index.html', {'form':form})
