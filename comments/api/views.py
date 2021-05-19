from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from comments.models import Comment
from comments.api.serializers import (
    CommentSerializer,
    CommentSerializerForCreate
)


class CommentViewSet(viewsets.GenericViewSet):
    """
    implement method for list, create, update and destroy
    no need for retrieve method, since no user requirement for such
    """

    serializer_class = CommentSerializerForCreate
    queryset = Comment.objects.all()

    def get_permissions(self):
        # return instance of AllowAny() or IsAuthenticated()
        if self.action == 'create':
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        data = {
            'user_id' : request.user.id,
            'tweet_id' : request.data.get('tweet_id'),
            'content': request.data.get('content'),
        }
        serializer = CommentSerializerForCreate(data=data)
        if not serializer.is_valid():
            return Response({
                'message': 'Please check input',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        comment = serializer.save()
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )