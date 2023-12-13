from django.core.exceptions import ImproperlyConfigured
from django.forms import DateInput, ModelForm, Select

from workplace import models


class TaskCreationForm(ModelForm):
    def __init__(self, author=None, *args, **kwargs):
        super(TaskCreationForm, self).__init__(*args, **kwargs)

        if author is None:
            raise ImproperlyConfigured("no task author specified")
        company_users = models.CompanyUser.objects.filter(
            company_id=author.company.id,
        ).exclude(user=author.user)

        choices = []

        for company_user in company_users:
            choices.append(
                (
                    company_user.user.id,
                    f"{company_user.user.first_name}"
                    f" {company_user.user.last_name}",
                ),
            )
        self.fields[models.Task.responsible.field.name].widget = Select(
            choices=choices,
        )

    class Meta:
        model = models.Task
        exclude = ["author"]
        widgets = {
            models.Task.deadline.field.name: DateInput(attrs={"type": "date"}),
        }
