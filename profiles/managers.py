from django.db import models


class ProfileManager(models.Manager):
    """
    Profile manager to define table level methods
    """

    def active(self):
        return self.get_queryset().filter(is_active=True)
