from django.db import models


class NotificationManager(models.Manager):

    def unread(self):
        return self.get_queryset().filter(unread=True)