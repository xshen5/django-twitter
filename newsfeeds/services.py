from newsfeeds.models import NewsFeed
from friendships.services import FriendshipService


class NewsFeedService(object):

    @classmethod
    def fanout_to_followers(cls, tweet):
        newsfeeds = [
            NewsFeed(user=follower, tweet=tweet)
            for follower in FriendshipService.get_followers(tweet.user)
            # notice here the tweet.user is the creator of tweet
        ]
        newsfeeds.append(NewsFeed(user=tweet.user, tweet=tweet))
        NewsFeed.objects.bulk_create(newsfeeds)
