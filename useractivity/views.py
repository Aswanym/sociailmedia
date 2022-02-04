from distutils.log import info
from functools import partial
from django.http.response import Http404
from django.shortcuts import render
from django.urls.resolvers import get_resolver
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from useractivity.models import Comment, Post, Love
from usermodule import serializers
from .serializers import (PostSerializer, AllPostViewSerializer,
                          CommentSerializer, CommentUpdateSerializer,
                          LikeSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
import logging
import pdb
# Create your views here.

logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()


#post create, update, delete
class AllPostViewSet(viewsets.ModelViewSet):
    serializer_class = AllPostViewSerializer
    queryset = Post.objects.all()


class PostCreateApiView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def create(self, request):
        try:
            data_copy = request.data.copy()
            data_copy.update(user=request.user.id)
            serializer = PostSerializer(data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)


class PostDetailsApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Http404

    def put(self, request, pk):
        try:
            post = self.get_object(pk)
            data_copy = request.data.copy()
            data_copy.update(user=request.user.id)
            serializer = PostSerializer(post, data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        try:
            post = self.get_object(pk)
            data_copy = request.data.copy()
            data_copy.update(user=request.user.id)
            serializer = PostSerializer(post, data=data_copy, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        instance = self.get_object(pk=pk)
        self.perform_destroy(instance)
        return Response({"message": "Post deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


#comment
class CreateCommentApiView(generics.ListCreateAPIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def create(self, request, pk):

        try:
            copy_data = request.data.copy()
            copy_data.update(post=pk)
            serializer = CommentSerializer(data=copy_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)


class CommentUpdateApiView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def destroy(self, request, pk):
        instance = self.get_object(pk=pk)
        self.perform_destroy(instance)
        return Response({"message": "comment deleted successfully"},
                        status=status.HTTP_204_NO_CONTENT)


#likes
class LikeApiView(generics.ListCreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Love.objects.all()

    def is_already_liked(self, pk):
        # pdb.set_trace()
        try:
            if Love.objects.filter(user=self.request.user.id,
                                   post=pk).exists():
                return True
            else:
                return False
        except Post.DoesNotExist:
            return Http404

    def create(self, request, pk):
        # pdb.set_trace()
        try:
            is_liked = self.is_already_liked(pk)
            if is_liked:
                return Response(
                    {
                        "message": "already liked this post",
                        "is_liked": is_liked
                    },
                    status=status.HTTP_200_OK)
            else:
                copy_data = request.data.copy()
                copy_data.update(post=pk, user=request.user.id)
                serializer = LikeSerializer(data=copy_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": "Something went wrong"},
                            status=status.HTTP_400_BAD_REQUEST)
