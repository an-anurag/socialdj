from django.db import models
from django.urls import reverse
from django.utils.timezone import now
# Create your models here.

from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    location = models.CharField(max_length=220, null=True, blank=True)
    bio = models.TextField(max_length=1000)
    picture = models.ImageField()
    mobile = models.CharField(max_length=10, null=True)
    address = models.TextField(max_length=1000, null=True)
    friends = models.ManyToManyField('Profile', blank=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile:detail', args=[self.user.username])


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # who sent the request
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')  # who will receive the request
    status = models.CharField(max_length=20, default='requested')
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)