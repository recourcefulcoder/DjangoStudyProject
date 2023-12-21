from django import forms
from django.core.exceptions import ImproperlyConfigured
import django.forms
from django.utils.translation import gettext as _

from workplace import models


class TaskCreationForm(django.forms.ModelForm):
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
        exclude = ["author", "state"]
        widgets = {
            models.Task.deadline.field.name: django.forms.DateInput(
                attrs={"type": "datetime-local"},
            ),
        }


class CompanyUpdateForm(django.forms.ModelForm):
    class Meta:
        model = models.Company
        exclude = ["working_days", "start_time", "end_time"]


class WeekDaysWidget(django.forms.MultiWidget):
    def decompress(self, value):
        if value:
            ans = []
            for day_ind in range(7):
                ans.append(value[day_ind] == "1")
            return ans
        return [True for _ in range(5)] + [False for _ in range(2)]


class WeekDaysField(django.forms.MultiValueField):
    def __init__(self, **kwargs):
        fields = (
            django.forms.BooleanField(required=False, label=_("mon")),
            django.forms.BooleanField(required=False, label=_("tues")),
            django.forms.BooleanField(required=False, label=_("wed")),
            django.forms.BooleanField(required=False, label=_("thur")),
            django.forms.BooleanField(required=False, label=_("fri")),
            django.forms.BooleanField(required=False, label=_("sat")),
            django.forms.BooleanField(required=False, label=_("sun")),
        )
        super().__init__(fields=fields, require_all_fields=False, **kwargs)

    def compress(self, data_list):
        res = ""
        for value in data_list:
            res += chr(ord("0") + value)
        return res


class CompanyScheduleForm(django.forms.Form):
    week_choices = WeekDaysField(
        widget=WeekDaysWidget(
            widgets=[django.forms.CheckboxInput for _ in range(7)],
        ),
    )

    start_time = django.forms.TimeField(widget=django.forms.TimeInput)
    end_time = django.forms.TimeField(widget=django.forms.TimeInput)


class TaskStageForm(django.forms.Form):
    pass


class InviteMemberForm(django.forms.Form):
    email = django.forms.EmailField()
