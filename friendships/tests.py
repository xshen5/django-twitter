from friendships.models import Friendship
from friendships.services import FriendshipService
from testing.testcases import TestCase


class FriendshipServiceTests(TestCase):

    def setUp(self):
        self.clear_cache()
        self.user1 = self.create_user('user1')
        self.user2 = self.create_user('user2')

    def test_get_followings(self):
        user3 = self.create_user('user3')
        user4 = self.create_user('user4')
        for to_user in [user3, user4, self.user2]:
            Friendship.objects.create(from_user=self.user1, to_user=to_user)
        # FriendshipService.invalidate_following_cache(from_user_id=self.user1.id)

        user_id_set = FriendshipService.get_following_user_id_set(self.user1.id)
        self.assertEqual(user_id_set, {user3.id, user4.id, self.user2.id})

        Friendship.objects.filter(from_user=self.user1.id, to_user=self.user2.id).delete()
        # FriendshipService.invalidate_following_cache(from_user_id=self.user1.id)
        user_id_set = FriendshipService.get_following_user_id_set(self.user1.id)
        self.assertEqual(user_id_set, {user3.id, user4.id})