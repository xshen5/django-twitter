from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import NewsFeedSerializer

class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # instead of using queryset() directly, we need to customize the method
        # since NewsFeed is only available to authenticated users
        return NewsFeed.objects.filter(user=self.request.user)

    def list(self, request):
        serializer = NewsFeedSerializer(
            self.get_queryset(),
            context={'request': request},
            many=True,
        )
        return Response({
            'newsfeeds': serializer.data
        }, status=status.HTTP_200_OK)