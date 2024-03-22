from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from urllib.parse import parse_qs
from .models import NewUser

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()
        query_string = parse_qs(scope["query_string"].decode())
        if b"token" in query_string:
            token = query_string[b"token"][0].decode()
            try:
                access_token = AccessToken(token)
                scope["user"] = await self.get_user(access_token)
            except:
                scope["user"] = AnonymousUser()
        return await self.inner(scope, receive, send)

    async def get_user(self, access_token):
        if not access_token.is_valid:
            return AnonymousUser()
        try:
            user_id = access_token.payload["user_id"]
            return await self.get_user_from_id(user_id)
        except:
            return AnonymousUser()

    async def get_user_from_id(self, user_id):
        try:
            return await NewUser.objects.get(id=user_id)
        except NewUser.DoesNotExist:
            return AnonymousUser()

def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))
