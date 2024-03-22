from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import NewUser
from django.conf import settings
import jwt


class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            user = await self.get_user_from_header()
            if user is not None and user.is_authenticated:
                chat_with_user = self.scope["url_route"]["kwargs"]["id"]
                user_ids = [int(user.id), int(chat_with_user)]
                user_ids = sorted(user_ids)
                self.room_group_name = f"chatting_with_user_{user_ids[0]}_{user_ids[1]}"  # Use both user IDs for uniqueness
                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name  # Use channel_name instead of channel_layer
                )
                await self.accept()
            else:
                await self.close()
        except Exception as e:
            print(f"Error during connection: {e}")
            await self.close()

    async def get_user_from_header(self):
        try:
            headers = dict(self.scope['headers'])
            auth_header = headers.get(b'authorization')
            if auth_header:
                auth_decoded = auth_header.decode().split()
                if len(auth_decoded) == 2 and auth_decoded[0] == 'Bearer':
                    token = auth_decoded[1]
                    return await self.get_user_from_token(token)  # Call asynchronously
            return None
        except Exception as e:
            print(f"Error during header processing: {e}")
            return None

    async def get_user_from_token(self, token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('id')
            user = NewUser.objects.get(pk=user_id)
            return user
        except jwt.ExpiredSignatureError:
            # Handle expired token
            return None
        except (jwt.InvalidTokenError, NewUser.DoesNotExist):
            # Handle invalid token or user not found
            return None



    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )

    async def disconnect(self, code):
        if self.channel_layer is not None:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({
            "message": message
        }))
