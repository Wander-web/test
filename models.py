from django.db import models
from django.contrib.auth.models import User


class Subj(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mobile = models.CharField(max_length=20, null=True, blank=True)
    prof_real = models.PositiveIntegerField(default='0',  blank=True)
    prof_intellect = models.PositiveIntegerField(default='0',  blank=True)
    prof_social = models.PositiveIntegerField(default='0',  blank=True)
    prof_conventional = models.PositiveIntegerField(default='0',  blank=True)
    prof_initiative = models.PositiveIntegerField(default='0',  blank=True)
    prof_art = models.PositiveIntegerField(default='0',  blank=True)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_instance(self):
        return self

    def __str__(self):
        return self.user.first_name
