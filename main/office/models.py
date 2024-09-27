from django.db import models

class Office(models.Model):
    office_name = models.CharField(max_length=254)
    office_description = models.TextField(
        blank=True, 
        null=True, 
        help_text="Enter a description of the office"
    )

    def __str__(self):
        return self.office_name
    
class Service(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=True, null=True,)
    service_name = models.CharField(max_length=254)
    service_description = models.TextField(
        blank=True,
        null=True,
        help_text="Enter a description of the service", 
    )

    def __str__(self):
        return self.service_name