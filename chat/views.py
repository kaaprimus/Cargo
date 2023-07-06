from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chat.models import Rooms, Messages

@login_required
def chatPage(request):
    rooms = Rooms.objects.all()

    return render(request, 'chat/index.html', {'rooms': rooms})

@login_required
def chatRoom(request, slug):
    room = Rooms.objects.get(slug=slug)
    messages = Messages.objects.filter(room=room)[0:25]

    return render(request, 'chat/chatPage.html', {'room': room, 'messages': messages})