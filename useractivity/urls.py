from django.urls import path
from useractivity.views import (PostCreateApiView, CreateCommentApiView,
                                PostDetailsApiView, CommentUpdateApiView,
                                LikeApiView)

urlpatterns = [
    path('create_post/', PostCreateApiView.as_view(), name='createpost'),
    path('post_details/<int:pk>/',
         PostDetailsApiView.as_view(),
         name='postdetails'),
    path('list_comment/', CreateCommentApiView.as_view(), name='listcomment'),
    path('create_comment/<int:pk>/',
         CreateCommentApiView.as_view(),
         name='createcomment'),
    path('update_comment/<int:pk>/',
         CommentUpdateApiView.as_view(),
         name='updatecomment'),
    path('like_post/<int:pk>/', LikeApiView.as_view(), name='likepost')
    #     path('like_post/<int:pk>/',
    #          LikeViewSet.as_view({
    #              'get': 'list',
    #              'post': 'create',
    #              'put': 'update',
    #              'delete': 'destroy'
    #          }),
    #          name='likepost'),
]