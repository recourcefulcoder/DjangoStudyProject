from django.core.exceptions import ImproperlyConfigured
from django import forms

from workplace import models


class TaskCreationForm(forms.ModelForm):
    def __init__(self, author=None, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)

        if author is None:
            raise ImproperlyConfigured("no task author specified")

        self.fields[
            models.Task.responsible.field.name
        ].queryset = models.CompanyUser.objects.filter(
            company_id=author.company.id,
        ).exclude(
            user=author.user,
        )

        self.fields[models.Task.responsible.field.name].empty_label = None

    class Meta:
        model = models.Task
        exclude = [models.Task.author.field.name]
        widgets = {
            models.Task.deadline.field.name: forms.DateTimeInput(),
        }
