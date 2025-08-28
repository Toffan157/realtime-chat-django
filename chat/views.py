from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .models import Room, Message
from .serializers import RoomSerializer, MessageSerializer


# --------------------
# Web views (UI)
# --------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('room_name').lower()
        
        if username and room_name:
            request.session['username'] = username
            request.session['room_name'] = room_name
            Room.objects.get_or_create(name=room_name)
            return redirect('chat', room_name=room_name)
    
    return render(request, 'login.html')


def chat_view(request, room_name):
    username = request.session.get('username')
    if not username:
        return redirect('login')
    
    room_name = room_name.lower()
    try:
        room = Room.objects.get(name=room_name)
        messages = Message.objects.filter(room=room).order_by('-timestamp')[:50]
    except Room.DoesNotExist:
        messages = []
    
    formatted_messages = []
    for message in messages:
        formatted_messages.append({
            'username': message.username,
            'content': message.content,
            'image': message.image.url if message.image else None,
            'content_type': message.content_type,
            'timestamp': message.timestamp,
            'is_system': message.username == 'System',
            'is_current_user': message.username == username,
        })
    
    context = {
        'room_name': room_name,
        'username': username,
        'messages': list(reversed(formatted_messages))  # oldest first
    }
    return render(request, 'chat.html', context)


# --------------------
# DRF API views
# --------------------

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RoomListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all rooms
    POST: Create a new room
    """
    queryset = Room.objects.all().order_by('-created_at')
    serializer_class = RoomSerializer


class MessageListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: Paginated list of messages for a room
    POST: Create a new message (text or image)
    """
    serializer_class = MessageSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        room_name = self.kwargs['room_name'].lower()
        room = get_object_or_404(Room, name=room_name)
        return Message.objects.filter(room=room).order_by('-timestamp')

    def perform_create(self, serializer):
        room_name = self.kwargs['room_name'].lower()
        room = get_object_or_404(Room, name=room_name)
        serializer.save(room=room)