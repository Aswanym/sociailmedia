from rest_framework import serializers
from useractivity.models import Comment, Love, Post
from django.contrib.auth import get_user_model

User = get_user_model()


class AllPostViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['description', 'post_image', 'location', 'user']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'comment_description', 'post']


class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'comment_description']


class LikeSerializer(serializers.ModelSerializer):

    is_liked = serializers.BooleanField()

    class Meta:
        model = Love
        fields = ['id', 'is_liked', 'post', 'user']
