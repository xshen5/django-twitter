from newsfeeds.models import NewsFeed
from friendships.models import Friendship
from rest_framework.test import APIClient
from testing.testcases import TestCase
from utils.paginations import EndlessPagination

NEWSFEED_URL = '/api/newsfeeds/'
POST_TWEETS_URL = '/api/tweets/'
FOLLOW_URL = '/api/friendships/{}/follow/'


class NewsFeedApiTests(TestCase):

    def setUp(self):
        self.clear_cache()

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
        self.assertEqual(len(response.data['results']), 0)
        # user's tweet should appear in its own newsfeeds
        self.user1_client.post(POST_TWEETS_URL, {
            'content': 'Hello World!'
        })
        response = self.user1_client.get(NEWSFEED_URL)
        self.assertEqual(len(response.data['results']), 1)
        # user can receive newsfeed from users it follows
        self.user1_client.post(FOLLOW_URL.format(self.user2.id))
        response = self.user2_client.post(POST_TWEETS_URL, {
            'content': 'Hello World!'
        })
        posted_tweet_id = response.data['id']
        response = self.user1_client.get(NEWSFEED_URL)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['tweet']['id'], posted_tweet_id)

    def test_pagination(self):
        page_size = EndlessPagination.page_size
        followed_user = self.create_user('followed')
        newsfeeds = []
        for i in range(page_size * 2):
            tweet = self.create_tweet(followed_user)
            newsfeed = self.create_newsfeed(user=self.user1, tweet=tweet)
            newsfeeds.append(newsfeed)

        newsfeeds = newsfeeds[::-1]

        # pull the first page
        response = self.user1_client.get(NEWSFEED_URL)
        self.assertEqual(response.data['has_next_page'], True)
        self.assertEqual(len(response.data['results']), page_size)
        self.assertEqual(response.data['results'][0]['id'], newsfeeds[0].id)
        self.assertEqual(response.data['results'][1]['id'], newsfeeds[1].id)
        self.assertEqual(
            response.data['results'][page_size - 1]['id'],
            newsfeeds[page_size - 1].id,
        )

        # pull the second page
        response = self.user1_client.get(
            NEWSFEED_URL,
            {'created_at__lt': newsfeeds[page_size - 1].created_at},
        )
        self.assertEqual(response.data['has_next_page'], False)
        results = response.data['results']
        self.assertEqual(len(results), page_size)
        self.assertEqual(results[0]['id'], newsfeeds[page_size].id)
        self.assertEqual(results[1]['id'], newsfeeds[page_size + 1].id)
        self.assertEqual(
            results[page_size - 1]['id'],
            newsfeeds[2 * page_size - 1].id,
        )

        # pull latest newsfeeds
        response = self.user1_client.get(
            NEWSFEED_URL,
            {'created_at__gt': newsfeeds[0].created_at},
        )
        self.assertEqual(response.data['has_next_page'], False)
        self.assertEqual(len(response.data['results']), 0)

        tweet = self.create_tweet(followed_user)
        new_newsfeed = self.create_newsfeed(user=self.user1, tweet=tweet)

        response = self.user1_client.get(
            NEWSFEED_URL,
            {'created_at__gt': newsfeeds[0].created_at},
        )
        self.assertEqual(response.data['has_next_page'], False)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], new_newsfeed.id)

    def test_user_cache(self):
        profile = self.user2.profile
        profile.nickname = 'user2_nickname'
        profile.save()

        self.assertEqual(self.user1.username, 'user1_newsfeed')
        self.create_newsfeed(self.user2, self.create_tweet(self.user1))
        self.create_newsfeed(self.user2, self.create_tweet(self.user2))

        response = self.user2_client.get(NEWSFEED_URL)
        results = response.data['results']
        self.assertEqual(results[0]['tweet']['user']['username'], 'user2_newsfeed')
        self.assertEqual(results[0]['tweet']['user']['nickname'], 'user2_nickname')
        self.assertEqual(results[1]['tweet']['user']['username'], 'user1_newsfeed')

        self.user1.username = 'user1'
        self.user1.save()
        profile.nickname = 'user1_nickname'
        profile.save()

        response = self.user2_client.get(NEWSFEED_URL)
        results = response.data['results']
        self.assertEqual(results[0]['tweet']['user']['username'], 'user2_newsfeed')
        self.assertEqual(results[0]['tweet']['user']['nickname'], 'user1_nickname')
        self.assertEqual(results[1]['tweet']['user']['username'], 'user1')
