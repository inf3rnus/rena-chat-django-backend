from http import cookies

from channels.auth import AuthMiddlewareStack
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class JsonWebTokenAuthenticationFromScope(BaseJSONWebTokenAuthentication):
    """
    Extracts the JWT from a channel scope (instead of an http request)
    """

    def get_jwt_value(self, scope):
        try:
            cookie = next(x for x in scope['headers'] if x[0].decode('utf-8') == 'cookie')[1].decode('utf-8')
            print('COOKIE IS: ', cookies.SimpleCookie(cookie)['JWT'].value)
            return cookies.SimpleCookie(cookie)['JWT'].value
        except:
            return None


class JsonTokenAuthMiddleware(BaseJSONWebTokenAuthentication):
    """
    Token authorization middleware for Django Channels 2
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):

        try:
            # Close old database connections to prevent usage of timed out connections
            close_old_connections()

            user, jwt_value = JsonWebTokenAuthenticationFromScope().authenticate(scope)
            scope['user'] = user
        except:
            scope['user'] = AnonymousUser()

        return self.inner(scope)


def JsonTokenAuthMiddlewareStack(inner):
    return JsonTokenAuthMiddleware(AuthMiddlewareStack(inner))
