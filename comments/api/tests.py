from testing.testcases import TestCase
from rest_framework.test import APIClient

COMMENT_URL = '/api/comments/'


class CommentApiTests(TestCase):

    def setUp(self):
        self.user1 = self.create_user('comment_user1')
        self.user1_client = APIClient()
        self.user1_client.force_authenticate(self.user1)
        self.user2 = self.create_user('comment_user2')
        self.user2_client = APIClient()
        self.user2_client.force_authenticate(self.user2)

        self.tweet = self.create_tweet(self.user2)

    def test_create(self):
        # user has to login
        response = self.anonymous_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 403)
        # has to have enough input
        response = self.user1_client.post(COMMENT_URL)
        self.assertEqual(response.status_code, 400)
        # has to provide tweet id
        response = self.user1_client.post(COMMENT_URL, {'content': 'default content'})
        self.assertEqual(response.status_code, 400)
        # has to provide content
        response = self.user1_client.post(COMMENT_URL, {'tweet_id': self.tweet.id})
        self.assertEqual(response.status_code, 400)
        # content's length must be less than 140
        response = self.user1_client.post(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'content': '1' * 141,
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual('content' in response.data['errors'], True)
        # success
        response = self.user1_client.post(COMMENT_URL, {
            'tweet_id': self.tweet.id,
            'content': '1',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['id'], self.user1.id)
        self.assertEqual(response.data['tweet_id'], self.tweet.id)
        self.assertEqual(response.data['content'], '1')