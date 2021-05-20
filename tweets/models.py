from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User
from utils.time_helpers import utc_now
from likes.models import Like


# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    # updated_at = models.DateTimeField(auto_now=True)
    # define composite index
    class Meta:
        index_together = (('user', 'created_at'),)
        ordering = ('user', '-created_at') # ordering with user_id ASC and created timestamp DESC

    @property
    def hours_to_now(self):
        return (utc_now() - self.created_at).seconds

    @property
    def like_set(self):
        return Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Tweet),
            object_id = self.id,
        ).order_by('-created_at')

    def __str__(self):
        # the following line return when calling print(tweet instance)
        return f'{self.created_at} {self.user} {self.content}'
