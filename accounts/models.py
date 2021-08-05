from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from accounts.listeners import user_changed, profile_changed


class UserProfile(models.Model):
    # using OneToOne field will create a unique index, and ensure that
    # there will not be multiple user profile points to the same user
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # Django does support ImageField, however, FileField can meet the same requiremnt
    # it will store the image as file with the URL points to the target
    avatar = models.FileField(null=True)
    # when a user get created, app will create an object of user profile
    # at this time users haven't got chance to setup nickname and other info.
    # set them to null=True
    nickname = models.CharField(null=True, max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.user, self.nickname)

    # def property method profile, insert it into User model
    # when we initialize a instance of User, and try to access profile, user_uninstance.profile
    # it will invoke get_or_create in UserProfile to retrieve profile object
    # this is actually a hacky way to retrieve profile by ultilizing python nature


def get_profile(user):
    from accounts.services import UserService

    if hasattr(user, '_cached_user_profile'):
        return getattr(user, '_cached_user_profile')
    #profile, _ = UserProfile.objects.get_or_create(user=user)
    profile = UserService.get_profile_through_cache(user.id)
    # utilize attribute of user object to cache info, this is to avoid calling DB many times
    # when retrieving the same user profile
    setattr(user, '_cached_user_profile', profile)
    return profile


# 给 User Model 增加了一个 profile 的 property 方法用于快捷访问
User.profile = property(get_profile)

# hook up with listeners to invalidate caches
pre_delete.connect(user_changed, sender=User)
post_save.connect(user_changed, sender=User)

pre_delete.connect(profile_changed, sender=UserProfile)
post_save.connect(profile_changed, sender=UserProfile)
