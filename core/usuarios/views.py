from django.conf import settings
from django.contrib.auth import authenticate
from datetime import date
from django.core.mail import send_mail, send_mass_mail
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.utils.crypto import get_random_string
from core.usuarios.api.serializers.password_serializers import ResetPasswordUserSerializer
from .api.serializers.usuarios_serializers import CustomTokenObtainPairSerializer, CustomUserSerializer
from .models import Usuario


def ocultar_email(email):
    partes = email.split('@')
    nombre = partes[0]
    dominio = partes[1]
    
    # Ocultar caracteres del nombre
    nombre_oculto = '*' * (len(nombre) - 7) + nombre[-7:]
    
    return f"{nombre_oculto}@{dominio}"


class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        usuario = authenticate(
            username = username,
            password = password
        )

        if usuario:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                usuario_serializer = CustomUserSerializer(usuario)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh': login_serializer.validated_data.get('refresh'),
                    'usuario': usuario_serializer.data,
                    'message': 'Inicio de Sesion Existoso'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_400_BAD_REQUEST)

class Logout(GenericAPIView):

    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(id = request.data.get('usuario', 0))
        if usuario.exists():
            RefreshToken.for_user(usuario.first())
            return Response({'message':'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)
        return Response({'error':'No existe este usuario'}, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPass(TokenObtainPairView):
    serializer_class = ResetPasswordUserSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        user = Usuario.objects.filter(username = username)
        if user:
            usuario = user.get()          
            reset_serializer = self.serializer_class(data = request.data)
            if reset_serializer.is_valid():
                        #### se genera la contraseña de 10 digitos
                password_new = get_random_string(length=10)
                correo = usuario.correo
                correo_oculto = ocultar_email(correo)
                        #### se envia la nueva contraseña al correo del usuario#
                subject = 'NOTIFICACION DE RESETEO DE CONTRASEÑA DEL SISTEMA DE TALENTO HUMANO'
                recipient_list = [usuario.correo]
                email_from = settings.EMAIL_HOST_USER
                mensaje_o = ('¡Hola!\n \nHemos recibido tu solicitud de cambio de contraseña.\n \nTu nueva contraseña es: ', password_new, '\n\nRecuerda mantener esta información en un lugar seguro y evitar compartirla con terceros. Si no realizaste este cambio, te recomendamos contactarnos de inmediato para garantizar la seguridad de tu cuenta.\n\n Saludos cordiales,')
                mensaje_trabajador = ' '.join(mensaje_o)
                correo_enviado = send_mail(subject, mensaje_trabajador, email_from, recipient_list, fail_silently=False,)
                if correo_enviado > 0:
                    ##se actualiza la contraseña del operador y clave provicional
                    usuario.set_password(password_new)
                    usuario.save()
                    Usuario.objects.filter(id=usuario.id).update(clave_temporal=True, fecha_clave=date.today())
                    mensaje = {'message': f'Se ha enviado un correo electrónico a {correo_oculto} con la nueva contraseña'}
                else:
                    mensaje_error ={'error': f'Hubo un problema al enviar el correo a {correo_oculto}.'}
            return Response(mensaje, status=status.HTTP_200_OK)
        mensaje_error = {'error':'No existe este usuario'}
        return Response(mensaje_error, status=status.HTTP_400_BAD_REQUEST)