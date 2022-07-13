from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from users.models import User, UserManager
from users.serializers import UserDetailSerializer, RegisterSerializer, UpdateSerializer,DeleteSerializer

# read bout ViewSet and routers
class UserViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        user = request.user  # deleting user
        # you custom logic #
        return super(UserViewSet, self).destroy(request, *args, **kwargs)


# Register API
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = User.objects.create_user(username, email, password)
        # return user
        return Response(
            UserDetailSerializer(user).data

        )
        # return Response({
        # "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
        # "token": AuthToken.objects.create(user)[1]
        # })


# Update API
class UpdateAPIView(generics.GenericAPIView):
    serializer_class = UpdateSerializer

    # def update(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(request.user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     username, email, password = (
    #         serializer.validated_data["username"],
    #         serializer.validated_data["email"],
    #         serializer.validated_data["password"],
    #         )
    #     user = User.objects.update_user(username, email, password, title=None)
    #     serializer.save()
    #     return Response(serializer.data)


    def put(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        username, email, password = (
            serializer.validated_data["username"],
            serializer.validated_data["email"],
            serializer.validated_data["password"],
        )
        user = get_object_or_404(User, pk=pk)
        user = User.objects.update_user(user, username, email, password)
        # return user
        return Response(
             UpdateSerializer(user).data
        )

class DeleteAPIView(generics.GenericAPIView):
    serializer_class = DeleteSerializer
    def delete(self, request,*args,**kwargs):
        user=self.request.user
        user.delete()
        # ВНИМАНИЕ тут надо сделать вместо этой хуйни isblocked=true
        return Response({"result":"user deleted"})