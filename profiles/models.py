from django.db import models
from django.urls import reverse
# Create your models here.

from django.contrib.auth.models import User
from .managers import ProfileManager
# Create your models here.
import uuid


class Profile(models.Model):
    """
    User profile
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    location = models.CharField(max_length=220, null=True, blank=True)
    bio = models.TextField(max_length=1000, blank=True)
    picture = models.ImageField(blank=True)
    mobile = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('profile:profile_detail', args=[self.slug])

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def set_active(self):
        if self.verified:
            self.is_active = True
            self.save()


class Connection(models.Model):
    """
    Follow model
    """

    STATUS_CHOICE = (
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follows')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    status = models.CharField(max_length=20, choices=STATUS_CHOICE, default='requested')
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return "Connection request from {} to {}".format(self.from_profile, self.to_profile)


Profile.add_to_class('following', models.ManyToManyField('self', through=Connection, related_name='followers'))