import socketio
from datetime import datetime, timezone
from asgiref.sync import sync_to_async
import base64, time, secrets
from django.core.files.base import ContentFile

from .models import Room, Message

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Store connected clients
connected_clients = {}

# Async ORM helpers
get_or_create_room = sync_to_async(Room.objects.get_or_create, thread_sensitive=True)
create_message = sync_to_async(Message.objects.create, thread_sensitive=True)

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    if sid in connected_clients:
        room_name = connected_clients[sid]['room']
        username = connected_clients[sid]['username']

        await save_and_broadcast_message(
            room_name=room_name,
            username='System',
            message=f'{username} has left the room'
        )
        del connected_clients[sid]


async def save_and_broadcast_message(room_name, username, message=None, image=None, content_type="text"):
    """Save message to DB and broadcast to room"""
    room_obj, created = await get_or_create_room(name=room_name)

    timestamp = datetime.now(timezone.utc).isoformat()
    msg_obj = None

    if username != 'System' or ('has joined' not in message and 'has left' not in message):
        if content_type == Message.IMAGE and image:
            # Decode base64 -> save file
            format, imgstr = image.split(';base64,')
            ext = format.split('/')[-1]  # e.g., "png", "jpeg"

            # Use timestamp + short random hex suffix
            file_name = f"img_{int(time.time())}_{secrets.token_hex(2)}.{ext}"
            image_file = ContentFile(base64.b64decode(imgstr), name=file_name)

            msg_obj = await create_message(
                room=room_obj,
                username=username,
                image=image_file,
                content_type=Message.IMAGE
            )
        else:
            msg_obj = await create_message(
                room=room_obj,
                username=username,
                content=message,
                content_type=Message.TEXT
            )

        timestamp = msg_obj.timestamp.isoformat()

    # Broadcast
    await sio.emit('message', {
        'username': username,
        'message': msg_obj.content if msg_obj and msg_obj.content else (message or ""),
        'image': msg_obj.image.url if msg_obj and msg_obj.image else None,
        'content_type': content_type,
        'timestamp': timestamp
    }, room=room_name)


@sio.event
async def join(sid, data):
    username = data.get('username')
    room_name = data.get('room').lower()

    if not username or not room_name:
        return False

    connected_clients[sid] = {'username': username, 'room': room_name}
    await sio.enter_room(sid, room_name)

    await save_and_broadcast_message(
        room_name=room_name,
        username='System',
        message=f'{username} has joined the room'
    )


@sio.event
async def send_message(sid, data):
    if sid not in connected_clients:
        return False

    user = connected_clients[sid]
    room_name = user['room']
    username = user['username']

    message = data.get('message')
    image = data.get('image')
    content_type = data.get('content_type', Message.TEXT)

    if not message and not image:
        return False

    await save_and_broadcast_message(
        room_name=room_name,
        username=username,
        message=message,
        image=image,
        content_type=content_type
    )