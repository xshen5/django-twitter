from rest_framework.test import APIClient
from testing.testcases import TestCase
from tweets.models import Tweet


# make sure to end the testing URL with '/', or it will return error 301
TWEET_LIST_API = '/api/tweets/'
TWEET_CREATE_API = '/api/tweets/'
TWEET_RETRIEVE_API = '/api/tweets/{}/'


class TweetApiTests(TestCase):

    def setUp(self):

        self.user1 = self.create_user('user1', 'user1@test.com')
        self.tweet1 = [
            self.create_tweet(self.user1)
            for i in range(3)
        ]
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1)

        self.user2 = self.create_user('user2', 'user2@test.com')
        self.tweet2 = [
            self.create_tweet(self.user2)
            for i in range(2)
        ]

    def test_list_api(self):
        # user_id is required for request
        response = self.anonymous_client.get(TWEET_LIST_API)
        self.assertEqual(response.status_code, 400)

        # request is good
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user1.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 3)
        response = self.anonymous_client.get(TWEET_LIST_API, {'user_id': self.user2.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['tweets']), 2)
        # tweets return in an order of it's created time
        self.assertEqual(response.data['tweets'][0]['id'], self.tweet2[1].id)
        self.assertEqual(response.data['tweets'][1]['id'], self.tweet2[0].id)

    def test_create_api(self):
        # user must be in login state
        response = self.anonymous_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 403)

        # the content of tweet must not be empty
        response = self.user1_client.post(TWEET_CREATE_API)
        self.assertEqual(response.status_code, 400)
        # content must be longer than 6
        response = self.user1_client.post(TWEET_CREATE_API, {'content': '123'})
        self.assertEqual(response.status_code, 400)
        # content must be shorter than 140
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': '0' * 141
        })
        self.assertEqual(response.status_code, 400)

        # post is good
        tweets_count = Tweet.objects.count()
        response = self.user1_client.post(TWEET_CREATE_API, {
            'content': 'this is a test tweet'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(Tweet.objects.count(), tweets_count+1)

    def test_retrieve(self):
        # tweet with id=-1 does not exist
        url = TWEET_RETRIEVE_API.format(-1)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 404)

        # 获取某个 tweet 的时候会一起把 comments 也拿下
        tweet = self.create_tweet(self.user1)
        url = TWEET_RETRIEVE_API.format(tweet.id)
        response = self.anonymous_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['comments']), 0)

        self.create_comment(self.user2, tweet, 'holy s***')
        self.create_comment(self.user1, tweet, 'hmm...')
        response = self.anonymous_client.get(url)
        self.assertEqual(len(response.data['comments']), 2)