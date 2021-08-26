from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from tweets.constants import TweetPhotoStatus, TWEET_PHOTO_STATUS_CHOICES
from utils.time_helpers import utc_now
from likes.models import Like
from utils.memcached_helper import MemcachedHelper
from django.db.models.signals import post_save
from utils.listeners import invalidate_object_cache
from tweets.listeners import push_tweet_to_cache


# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # when adding new fields, make sure to allow null=True, otherwise the default=0 statement will be
    # executed against the entire table, which increase the cost of the migration.
    # Since migration will lock the table itself, it will stop user from accessing tweet table
    likes_count = models.IntegerField(default=0, null=True)
    comments_count = models.IntegerField(default=0, null=True)

    # updated_at = models.DateTimeField(auto_now=True)
    # define composite index
    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at')  # ordering with user_id ASC and created timestamp DESC

    @property
    def hours_to_now(self):
        return (utc_now() - self.created_at).seconds

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Tweet),
            object_id=self.id,
        ).order_by('-created_at')

    def __str__(self):
        # the following line return when calling print(tweet instance)
        return f'{self.created_at} {self.user} {self.content}'

    @property
    def cached_user(self):
        return MemcachedHelper.get_object_through_cache(User, self.user_id)


class TweetPhoto(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.SET_NULL, null=True)

    # 谁上传了这张图片，这个信息虽然可以从 tweet 中获取到，但是重复的记录在 Image 里可以在
    # 使用上带来很多遍历，比如某个人经常上传一些不合法的照片，那么这个人新上传的照片可以被标记
    # 为重点审查对象。或者我们需要封禁某个用户上传的所有照片的时候，就可以通过这个 model 快速
    # 进行筛选
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    file = models.FileField()
    order = models.IntegerField(default=0)

    # state of image, used for process of audit
    status = models.IntegerField(
        default=TweetPhotoStatus.PENDING,
        choices=TWEET_PHOTO_STATUS_CHOICES,
    )

    # softdelete: when deleting a image, mark the requested file as deleted, and only deleted after a while,
    # Pro: deleting image async can help increase the performance when deleting a tweet.
    has_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('user', 'created_at'),
            ('has_deleted', 'created_at'),
            ('status', 'created_at'),
            ('tweet', 'order'),
        )

    def __str__(self):
        return f'{self.tweet_id}: {self.file}'


post_save.connect(invalidate_object_cache, sender=Tweet)
post_save.connect(push_tweet_to_cache, sender=Tweet)
