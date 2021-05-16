from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from tweets.models import Tweet
from tweets.api.serializers import TweetSerializer, TweetCreateSerializer


class TweetViewSet(viewsets.GenericViewSet,
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin):
    """
    API endpoint that allows user to create tweets and list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer

    def get_permissions(self):
        if self.action == 'list':
            return[permissions.AllowAny()]
        return[permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        overload create function, to default the login user as a tweet.user
        """
        serializer = TweetCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Please check input',
                'errors': serializer.errors,
            }, status=400)
        tweet = serializer.save()
        return Response(TweetSerializer(tweet).data, status=201)

    def list(self, request, *args, **kwargs):
        """
        overloading list function, make user_id as a requirement to filter
        """
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)

        """
        The above line will be interpreted as following SQL:'
        select * from twitter_tweets where user_id=xxx order by created_at DESC
        this SQL query will be using composite index of user_id and created_at
        """

        tweets = Tweet.objects.filter(user_id=request.query_params['user_id']).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        # usually response in JSON format should be included in hash
        # instead of a list
        return Response({'tweets': serializer.data})