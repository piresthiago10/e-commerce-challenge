from account.api.serializers import UsersSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from account.models import APIAccountManager
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class UserCreateViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = UsersSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            account_manager = APIAccountManager()
            new_user = account_manager.create_user(
                username=serializer.validated_data.get('username'),
                password=serializer.validated_data.get('password'),
                email=serializer.validated_data.get('email')
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    http_method_names = ['get', 'put', 'delete']
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]