from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile, Showroom

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Option: Use a default showroom.
        # Make sure a Showroom exists. You can choose a showroom by some criteria.
        default_showroom = Showroom.objects.first()  
        UserProfile.objects.create(user=instance, showroom=default_showroom)
