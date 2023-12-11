from django.forms import ModelForm
from workplace import models


class TaskCreationForm(ModelForm):
    class Meta:
        model = models.Task
        exclude = ["manager"]
