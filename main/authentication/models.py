# authentication/models.py
from django.db import models
from django.contrib.auth.models import User
from office.models import Office

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.office.office_name}"
