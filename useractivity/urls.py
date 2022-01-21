from django.urls import path
from useractivity.views import (PostCreateApiView, PostUpdateApiView, 
                                PostDeleteApiView, CreateCommentApiView, CommentUpdateApiView, LikeViewSet)
urlpatterns =[

    path('create_post/', PostCreateApiView.as_view(), name='createpost'),
    path('update_post/<int:pk>/', PostUpdateApiView.as_view(), name='updatepost'),
    path('delete_post/<int:pk>/', PostDeleteApiView.as_view(), name='deletepost'),

    path('list_comment/', CreateCommentApiView.as_view(), name='listcomment'),
    path('create_comment/<int:pk>/', CreateCommentApiView.as_view(), name='createcomment'),
    path('update_comment/<int:pk>/', CommentUpdateApiView.as_view(), name='updatecomment'),

    path('like_post/<int:pk>/', LikeViewSet.as_view({'post':'create','put':'update','delete': 'destroy'}), name='likepost'),

]