from django.contrib.auth.models import User
from django.db import models
from utils.memcached_helper import MemcachedHelper
from tweets.models import Tweet
from django.db.models.signals import post_save
from newsfeeds.listeners import push_newsfeed_to_cache


class NewsFeed(models.Model):
    # note that the user in the model is to store the users who can view this post
    # instead of the user who created the post
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (('user', 'created_at'),)
        unique_together = (('user', 'tweet'),)
        ordering = ('user', '-created_at',)

    def __str__(self):
        return f'{self.created_at} inbox of {self.user}: {self.tweet}'

    def cached_tweet(self):
        return MemcachedHelper.get_object_through_cache(Tweet, self.tweet_id)

post_save.connect(push_newsfeed_to_cache, sender=NewsFeed)

