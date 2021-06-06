from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify

from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    On user registration, it creates the user profile
    and updates the slug
    """
    if created:
        profile = Profile.objects.create(user=instance)
        profile.slug = slugify(instance.username)
        profile.save()