from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

# Create your models here.

# Model for user profiles
class User(AbstractUser):
    meeting_count = models.IntegerField(default=0)
    speech_count = models.IntegerField(default=0)
    executive = models.BooleanField(default=False)
    last_speech = models.DateTimeField(null=True)

# Model for each meeting
class Meeting(models.Model):
    id = models.AutoField(primary_key = True)
    starttime = models.DateTimeField()

    def __str__(self):
        return f"{self.id}: {self.starttime}"


class Rolelist(models.Model):
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE, related_name="rolelist")
    facilitator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="facilitator", null=True)
    toastmaster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="toastmaster", null=True)
    geneval = models.ForeignKey("User", on_delete=models.CASCADE, related_name="geneval", null=True)
    saa = models.ForeignKey("User", on_delete=models.CASCADE, related_name="saa", null=True)
    chair = models.ForeignKey("User", on_delete=models.CASCADE, related_name="chair", null=True)

    speaker1 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="speaker1", null=True)
    speaker2 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="speaker2", null=True)
    speaker3 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="speaker3", null=True)
    eval1 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="eval1", null=True)
    eval2 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="eval2", null=True)
    eval3 = models.ForeignKey("User", on_delete=models.CASCADE, related_name="eval3", null=True)

    ttmaster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ttmaster", null=True)
    tteval = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tteval", null=True)

    timer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="timer", null=True)
    ah_counter = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ah_counter", null=True)
    quizmaster = models.ForeignKey("User", on_delete=models.CASCADE, related_name="quizmaster", null=True)

    absences = models.BooleanField(default=0)

    def __str__(self):
        return f"Rolelist {self.meeting}: facilitator-{self.facilitator}, toast-{self.toastmaster}"

    
class Attendee(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="absences")
    meeting = models.ForeignKey("Meeting", on_delete=models.CASCADE, related_name="absenses")
    status = models.CharField(max_length=1, default="U")

    def __str__(self):
        return f"Meeting {self.meeting.id}: {self.user} {self.status}"

