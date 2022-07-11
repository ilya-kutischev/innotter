from django.shortcuts import render
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from users.models import User
from users.serializers import UserDetailSerializer


# read bout ViewSet and routers
class UserViewSet(ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    # @action
    # def retrieveUser(self, request, pk=None):
    #     queryset = User.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = UserDetailSerializer(user)
    #     return Response(serializer.data)

    def create(self, request):
        serializer = UserDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # @api_view(['POST'])
    # def updateUser(self, request, pk=None):
    #     queryset = User.objects.all()
    #     serializer = UserDetailSerializer(queryset, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(serializer.data)
    #
    # @api_view(['DELETE'])
    # def deleteUser(self, request, pk=None):
    #     user = get_object_or_404(User, pk=pk)
    #     user.delete()
    #     return Response(status=204)
