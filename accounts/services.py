from accounts.models import UserProfile
from django.conf import settings
from django.core.cache import caches
from twitter.cache import USER_PROFILE_PATTERN

cache = caches['testing'] if settings.TESTING else caches['default']


class UserService:


    @classmethod
    def get_profile_through_cache(cls, user_id):
        key = USER_PROFILE_PATTERN.format(user_id=user_id)
        # try hit cache
        profile = cache.get(key)
        # if hit, return to user
        if profile is not None:
            return profile

        # if miss, get from DB
        # since using get_or_create, not need to try-catch
        profile, _ = UserProfile.objects.get_or_create(user_id=user_id)
        cache.set(key, profile)
        return profile

    @classmethod
    def invalidate_profile(cls, user_id):
        key = USER_PROFILE_PATTERN.format(user_id=user_id)
        cache.delete(key)