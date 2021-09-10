from django_hbase import models


class HBaseFollowing(models.HBaseModel):
    """
    store accounts followed by from_user_id
    row_key order: from_user_id + created_at together
    support following queries:
    - all accounts followed by A order by following timestamp
    - all accounts followed by A as of a timestamp
    - the first X number of accounts followed by A after/before a timestamp
    """
    from_user_id = models.IntegerField(reverse=True)
    created_at = models.TimestampField()

    # column key
    to_user_id = models.IntegerField(column_family='cf')

    class Meta:
        table_name = 'twitter_followings'
        row_key = ('from_user_id', 'created_at')


class HBaseFollower(models.HBaseModel):
    """
    store all accounts following to_user_id, order row_key by to_user_id + created_at
    support following queries:
    - all followers of A ordered by starting time
    - all followers of A as of a timestamp
    - X number of follower of A before/after a timestamp
    """
    # row key
    to_user_id = models.IntegerField(reverse=True)
    created_at = models.TimestampField()

    # column key
    from_user_id = models.IntegerField(column_family='cf')

    class Meta:
        row_key = ('to_user_id', 'created_at')
        table_name = 'twitter_followers'
