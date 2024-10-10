from django.db import models
from django.contrib.auth.models import User
from office.models import Office

class Profile(models.Model):
    role_choices = [
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('employee', 'Employee'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    office = models.ForeignKey(Office, on_delete=models.CASCADE, null=True, blank=True)
    role = models.CharField(max_length=20, choices=role_choices, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.office.office_name if self.office else 'No Office'}"
