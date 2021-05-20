from rest_framework import serializers

from accounts.api.serializers import UserSerializer
from tweets.models import Tweet
from comments.api.serializers import CommentSerializer


class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'content', 'created_at')


class TweetSerializerWithComments(TweetSerializer):
    comments = CommentSerializer(source='comment_set', many=True)

    class Meta:
        model = Tweet
        fields = ('id', 'user', 'content', 'created_at', 'comments')


class TweetCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=6, max_length=140)

    class Meta:
        model = Tweet
        fields = ('content',)

    def create(self, validated_data):
        user = self.context['request'].user
        content = validated_data['content']
        tweet = Tweet.objects.create(user=user, content=content)
        return tweet
