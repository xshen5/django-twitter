from django.test import TestCase as DjangoTestCase
from django.contrib.auth.models import User
from tweets.models import Tweet
from comments.models import Comment


class TestCase(DjangoTestCase):
    """
    Adding a customized testcase class, so we can reuse this in other unittests
    to create user and  tweets for unit tests
    """
    def create_user(self, username, email=None, password=None):
        if email is None:
            email = '{}@test.com'.format(username)
        if password is None:
            password = 'generic password'
        return User.objects.create_user(username, email, password)

    def create_tweet(self, user, content=None):
        if content is None:
            content = 'default tweet content'
        return Tweet.objects.create(user=user, content=content)

    def create_comment(self, user, tweet, content=None):
        if content is None:
            content = 'default comment content'
        return Comment.objects.create(user=user, tweet_id=tweet, content=content)
