from django.db import models

from profiles.models import Profile
from django.utils.timesince import timesince
import uuid


class Activity(models.Model):

    """
    Possible activity type
    connection
    comment

    possible subtypes
    accept
    reject
    comment
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    activity = models.CharField(max_length=128)
    subtype = models.CharField(max_length=128)
    verb = models.CharField(max_length=1024)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural = 'Activities'

    def __str__(self):
        return str(self.id)

    @classmethod
    def get_activity(cls, activity=None, subtype=None):
        if subtype:
            return cls.objects.filter(activity__iexact=activity, subtype__iexact=subtype).first()
        if not subtype:
            return cls.objects.filter(activity__iexact=activity).first()


class Notifications(models.Model):
    """
    Model for User activity notification
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    actor = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, related_name='notifications_sent')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False, related_name='notifications')
    unread = models.BooleanField(default=True, blank=False, db_index=True)
    activity_type = models.ForeignKey(to=Activity, on_delete=models.SET_NULL, null=True)
    event_id = models.UUIDField(default=uuid.uuid4)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)

    @classmethod
    def notify(cls, actor, recipient, activity_type, event_id, description):
        cls.objects.create(
            actor=actor,
            recipient=recipient,
            activity_type=activity_type,
            event_id=event_id,
            description=description
        )

    def timesince(self, now=None):
        return timesince(self.created, now)

    def mark_as_read(self):
        if self.unread:
            self.unread = False
            self.save()

    def mark_as_unread(self):
        if not self.unread:
            self.unread = True
            self.save()
