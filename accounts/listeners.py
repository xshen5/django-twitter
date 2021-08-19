
def profile_changed(sender, instance, **kwargs):
    # import only in function to avoid cyclic dependencies
    from accounts.services import UserService
    UserService.invalidate_profile(instance.user_id)