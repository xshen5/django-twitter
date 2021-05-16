from django.contrib.auth.models import User
from django.test import TestCase
from tweets.models import Tweet
from datetime import timedelta
from utils.time_helpers import utc_now

# Create a test for hours_to_now in Tweet model


class TweetTests(TestCase):

    def test_hours_to_now(self):
        userone = User.objects.create_user(username='userone')
        tweet = Tweet.objects.create(user=userone, content='test tweet')
        tweet.created_at = utc_now() - timedelta(hours=10)
        tweet.save()
        self.assertEqual(tweet.hours_to_now, 36000)
