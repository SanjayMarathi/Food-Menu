from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save # NEW: Import post_save signal
from django.dispatch import receiver # NEW: Import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='profilepic.jpg', upload_to='profile_pictures')
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user.username

# NEW: Signal to create a Profile when a new User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# NEW: Signal to save the Profile when the User object is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # This prevents the error on first access after creation, but handles saves on subsequent updates.
    # We must ensure the profile exists before trying to save it.
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        # If the profile still doesn't exist (e.g., from an old user without the create signal)
        # the defensive coding in the view already handles this, but we can prevent a
        # potential error here too if we were to save the user elsewhere.
        pass