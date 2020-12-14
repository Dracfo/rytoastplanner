from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

# Create your models here.

#Function to return 'deleted' for related objects when a user is deleted
def get_deleted_user_instance():
    return User.objects.get(username='deleted')


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
    wod = models.CharField(max_length=50, default=None, null=True)
    theme = models.CharField(max_length=50, default=None, null=True)

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


# List of the different kinds of bugs users can submit
BUG_TYPES = [
    ('1 Critical', 'Critical'),
    ('2 Serious', 'Serious'),
    ('3 Normal', 'Normal'),
    ('4 Cosmetic/Enhancement', 'Cosmetic/Enhancement'),
    ('5 Suggestion', 'Suggestion'),
]


# Form to submit a bug report
class BugForm(forms.Form):
    contact_info = forms.CharField(label='Your Contact Information', required=False, max_length=256, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'How can the admin contact you if they need more information?'}))
    bug_type = forms.ChoiceField(
        required=True,
        choices=BUG_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    bug_location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Where did you find the bug?'}))
    bug_description = forms.CharField(max_length=2200, required=True, label="Bug Description", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Describe what happened'}))


class Buglist(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey("User", on_delete=models.SET(get_deleted_user_instance), related_name="bugs_reported", null=True, blank=True)
    contact_info = models.CharField(max_length=256, null=True, blank=True)
    bug_type = models.CharField(max_length=100, null=True, blank=True)
    bug_location = models.CharField(max_length=100, null=True, blank=True)
    bug_description = models.CharField(max_length=2200, null=True, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"Bug {self.id}: {self.bug_type} in {self.bug_location} reported by {self.user} on {self.date_reported}"

