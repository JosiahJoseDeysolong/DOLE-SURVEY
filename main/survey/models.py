# models.py
from django.db import models
from office.models import Office, Service

class Survey(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class SexChoices(models.TextChoices):
        MALE = "M", 'Male'
        FEMALE = "F", 'Female'

    class ClientTypeChoices(models.TextChoices):
        CITIZEN = "CM", 'Citizen (Mamayan)'
        BUSINESS = "B", 'Business'
        GOVERNMENT = "G", 'Government (Employee or another agency)'

    class ScaleChoices(models.IntegerChoices):
        NA = 0, 'N/A'
        STRONGLY_DISAGREE = 1, 'Strongly Disagree'
        DISAGREE = 2, 'Disagree'
        NEUTRAL = 3, 'Neutral'
        AGREE = 4, 'Agree'
        STRONGLY_AGREE = 5, 'Strongly Agree'

    class CC1Choices(models.IntegerChoices):
        KNOW_AND_SEEN = 1, 'I know what a CC is and I saw this office\'s CC.'
        KNOW_NOT_SEEN = 2, 'I know what a CC is but I did NOT see this office\'s CC.'
        LEARNED_WHEN_SEEN = 3, 'I learned of the CC only when I saw this office\'s CC.'
        DO_NOT_KNOW_NOT_SEEN = 4, 'I do not know what a CC is and I did not see one in this office.'

    class CC2Choices(models.IntegerChoices):
        EASY_TO_SEE = 1, 'Easy to see'
        SOMEWHAT_EASY_TO_SEE = 2, 'Somewhat easy to see'
        DIFFICULT_TO_SEE = 3, 'Difficult to see'
        NOT_VISIBLE = 4, 'Not visible at all'
        NA = 5, 'N/A'

    class CC3Choices(models.IntegerChoices):
        HELPED_VERY_MUCH = 1, 'Helped very much'
        SOMEWHAT_HELPED = 2, 'Somewhat helped'
        DID_NOT_HELP = 3, 'Did not help'
        NA = 4, 'N/A'

    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=254,null=True, blank=True)
    client_type = models.CharField(max_length=2, choices=ClientTypeChoices.choices)
    date = models.DateField()
    sex = models.CharField(max_length=1, choices=SexChoices.choices)
    age = models.PositiveIntegerField()
    region = models.CharField(max_length=255)

    cc1 = models.IntegerField(choices=CC1Choices.choices)
    cc2 = models.IntegerField(choices=CC2Choices.choices)
    cc3 = models.IntegerField(choices=CC3Choices.choices)

    sqd0 = models.IntegerField(choices=ScaleChoices.choices)
    sqd1 = models.IntegerField(choices=ScaleChoices.choices)
    sqd2 = models.IntegerField(choices=ScaleChoices.choices)
    sqd3 = models.IntegerField(choices=ScaleChoices.choices)
    sqd4 = models.IntegerField(choices=ScaleChoices.choices)
    sqd5 = models.IntegerField(choices=ScaleChoices.choices)
    sqd6 = models.IntegerField(choices=ScaleChoices.choices)
    sqd7 = models.IntegerField(choices=ScaleChoices.choices)
    sqd8 = models.IntegerField(choices=ScaleChoices.choices)

    suggestions = models.TextField()

    def __str__(self):
        office_name = self.office.office_name
        return f"Survey on {self.date} - {office_name}"
