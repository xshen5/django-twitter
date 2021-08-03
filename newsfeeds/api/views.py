from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from utils.paginations import EndlessPagination
from newsfeeds.models import NewsFeed
from newsfeeds.api.serializers import NewsFeedSerializer

class NewsFeedViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = EndlessPagination

    def get_queryset(self):
        # instead of using queryset() directly, we need to customize the method
        # since NewsFeed is only available to authenticated users
        return NewsFeed.objects.filter(user=self.request.user)

    def list(self, request):
        queryset = NewsFeed.objects.filter(user=self.request.user)
        page = self.paginate_queryset(queryset)
        serializer = NewsFeedSerializer(
            page,
            context={'request': request},
            many=True,
        )
        return self.get_paginated_response(serializer.data)