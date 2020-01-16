from django.db import models

# Create your models here.
class Friend(models.Model):
    # Remove nullability later.
    user_profile = models.ForeignKey(CustomUser, related_name="owner", on_delete=models.CASCADE, null=True)
    friends = models.ManyToManyField(CustomUser)
    pending_friends = models.ManyToManyField(CustomUser, related_name="pending_friends")
    requested_friends = models.ManyToManyField(CustomUser, related_name="requested_friends")

    @classmethod
    def add_pending_friend(cls, current_user, new_friend):
        # Add the current user to the pending friends of the recipient.
        Friend, created = cls.objects.get_or_create(user_profile_id=new_friend.id)
        Friend.pending_friends.add(current_user)

        # Add the requested friend to the list of friends that have been requested.
        Friend, created = cls.objects.get_or_create(user_profile_id=current_user.id)
        Friend.requested_friends.add(new_friend)

    @classmethod
    def confirm_friend(cls, current_user, new_friend):
        # Get or create returns a tuple with the first object being the object returned
        # the second field is a boolean which tells you if an object was created.
        Friend, created = cls.objects.get_or_create(user_profile_id=current_user.id)
        # Check if friend is pending to make sure they initiated the request.
        # CustomUser record is then removed from the pending_friends table.
        if Friend.pending_friends.get(pk=new_friend.id):
            # Send request to the destination user
            Friend.friends.add(new_friend)
            Friend.pending_friends.remove(new_friend)
            Friend.requested_friends.remove(new_friend)
            # Set the recipient as a member of the requestor's pending list
            Friend, created = cls.objects.get_or_create(user_profile_id=new_friend.id)
            Friend.friends.add(current_user)
            Friend.pending_friends.remove(current_user)
            Friend.requested_friends.remove(current_user)


    @classmethod
    def remove_friend(cls, current_user, new_friend):
        Friend, created = cls.objects.get_or_create(user_profile_id=current_user.id)
        Friend.friends.remove(new_friend)

        Friend, created = cls.objects.get_or_create(user_profile_id=new_friend.id)
        Friend.friends.remove(current_user)
        

    @classmethod
    def remove_pending_friend(cls, current_user, new_friend):
        Friend, created = cls.objects.get_or_create(user_profile_id=current_user.id)
        Friend.pending_friends.remove(new_friend)

        Friend, created = cls.objects.get_or_create(user_profile_id=new_friend.id)
        Friend.requested_friends.remove(current_user)

    @classmethod
    def remove_requested_friend(cls, current_user, new_friend):
        Friend, created = cls.objects.get_or_create(user_profile_id=new_friend.id)
        Friend.pending_friends.remove(current_user)

        Friend, created = cls.objects.get_or_create(user_profile_id=current_user.id)
        Friend.requested_friends.remove(new_friend)
    

    def __str__(self):
        return str(self.user_profile)