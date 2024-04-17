from rest_framework import status, authentication, exceptions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authentication import get_authorization_header

from core.usuarios.authentication import ExpiringTokenAuthentication

class Authentication(authentication.BaseAuthentication):
    usuario = None

    def get_user(self, request):

        token = get_authorization_header(request).split()

        if token:
            try:
                token = token[1].decode()
            except:
                return None
            
            token_expire = ExpiringTokenAuthentication()
            usuario = token_expire.authenticate_credentials(token)

            if usuario != None:
                self.usuario = usuario
                return usuario
        return None
    
    def authenticate(self, request):
        self.get_user(request)
        if self.usuario is None:
            raise exceptions.AuthenticationFailed('No se han enviado las credenciasles.')
        return (self.usuario, 1)