from datetime import timedelta

from testing.testcases import TestCase
from tweets.constants import TweetPhotoStatus
from tweets.models import TweetPhoto
from utils.time_helpers import utc_now


# Create a test for hours_to_now in Tweet model


class TweetTests(TestCase):

    def setUp(self):
        self.user = self.create_user('user1')
        self.tweet = self.create_tweet(self.user)
        self.comment = self.create_comment(self.user, self.tweet)

    def test_hours_to_now(self):
        self.tweet.created_at = utc_now() - timedelta(hours=10)
        self.tweet.save()
        self.assertEqual(self.tweet.hours_to_now, 36000)

    def test_like_test(self):
        self.create_like(self.user, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        self.create_like(self.user, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 1)

        user2 = self.create_user('user2')
        self.create_like(user2, self.tweet)
        self.assertEqual(self.tweet.like_set.count(), 2)


def test_create_photo(self):
    # 测试可以成功创建 photo 的数据对象
    photo = TweetPhoto.objects.create(
        tweet=self.tweet,
        user=self.linghu,
    )
    self.assertEqual(photo.user, self.linghu)
    self.assertEqual(photo.status, TweetPhotoStatus.PENDING)
    self.assertEqual(self.tweet.tweetphoto_set.count(), 1)
