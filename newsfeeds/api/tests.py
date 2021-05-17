from newsfeeds.models import NewsFeed
from friendships.models import Friendship
from rest_framework.test import APIClient
from testing.testcases import TestCase

NEWSFEED_URL = '/api/newsfeeds/'
POST_TWEETS_URL = '/api/tweets/'
FOLLOW_URL = '/api/friendships/{}/follow/'


class NewsFeedApiTests(TestCase):

    def setUp(self):
        self.anonymous_client = APIClient()

        self.user1 = self.create_user('user1_newsfeed')
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.create_user('user2_newsfeed')
        self.user2_client = APIClient()
        self.user2_client.force_authenticate(self.user2)

        # create followings and followers for user2
        for i in range(2):
            follower = self.create_user('user2_follower{}'.format(i))
            Friendship.objects.create(from_user=follower, to_user=self.user2)
        for i in range(3):
            following = self.create_user('user2_following{}'.format(i))
            Friendship.objects.create(from_user=self.user2, to_user=following)

    def test_list(self):
        # user needs to login
        response = self.anonymous_client.get(NEWSFEED_URL)
        self.assertEqual(response.status_code, 403)
        # POST method not allowed
        response = self.user1_client.post(NEWSFEED_URL)
        self.assertEqual(response.status_code, 405)
        # the newsfeed should be empty when initialized
        response = self.user1_client.get(NEWSFEED_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['newsfeeds']), 0)
        # user's tweet should appear in its own newsfeeds
        self.user1_client.post(POST_TWEETS_URL, {
            'content': 'Hello World!'
        })
        response = self.user1_client.get(NEWSFEED_URL)
        self.assertEqual(len(response.data['newsfeeds']), 1)
        # user can receive newsfeed from users it follows
        self.user1_client.post(FOLLOW_URL.format(self.user2.id))
        response = self.user2_client.post(POST_TWEETS_URL, {
            'content': 'Hello World!'
        })
        posted_tweet_id = response.data['id']
        response = self.user1_client.get(NEWSFEED_URL)
        self.assertEqual(len(response.data['newsfeeds']), 2)
        self.assertEqual(response.data['newsfeeds'][0]['tweet']['id'], posted_tweet_id)

