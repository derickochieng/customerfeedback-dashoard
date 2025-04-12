from django.db import models
from django.contrib.auth.models import User

# 1. Showroom Model
class Showroom(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name

# 2. UserProfile Model: Links a Django User to a Showroom
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s profile"

# 3. Feedback Model: Captures the feedback source and links to a showroom
# Define choices for feedback source
SOURCE_CHOICES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('tiktok', 'TikTok'),
    ('google_ads', 'Google Ads'),
    ('referral', 'Friend Referral'),
    ('passing', 'Just Passing By'),
]

class Feedback(models.Model):
    showroom = models.ForeignKey(Showroom, on_delete=models.CASCADE)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.showroom.name} - {self.source}"

