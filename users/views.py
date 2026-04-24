from rest_framework import generics,permissions
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response

from django.db.models.functions import Concat
from django.db.models import Value, CharField

from .models import User
from .serializers import RegisterSerializer,UserSerializer




class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'register'


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)


        user = User.objects.annotate(
            display_name=Concat('name', Value(' ('), 'username', Value(')'), output_field=CharField(),)).get(pk=instance.pk)

        data['display_name'] = user.display_name
        return Response(data)
