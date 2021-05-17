from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # when record deleted, set this field to true instead of deleting it
        null=True,  # allow this field to be null
        related_name='following_friendship_set',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='followed_friendship_set',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            # all followings of a user, order by following time asc
            ('from_user_id', 'created_at'),
            # all follower of a user, order by following time asc
            ('to_user_id', 'created_at'),
        )
        unique_together = (
            ('from_user_id', 'to_user_id')
        )

    def __str__(self):
        return '{} followed {}'.format(self.from_user_id, self.to_user_id)
