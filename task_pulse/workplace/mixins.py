from django.contrib import messages
from django.contrib.auth import mixins
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _

from workplace import models


class CompanyUserRequiredMixin(mixins.AccessMixin):
    permission_denied_message = _("You are not a participant in this company")

    def dispatch(self, request, *args, **kwargs):
        company = self.get_company()
        company_user = self.get_company_user(company.id)

        if not company_user:
            messages.add_message(
                request,
                messages.ERROR,
                type(self).permission_denied_message,
            )
            return redirect("homepage:homepage")

        return super().dispatch(request, *args, **kwargs)

    def get_company(self):
        return get_object_or_404(
            models.Company,
            pk=self.kwargs.get("company_id"),
        )

    def get_company_user(self, company_id):
        return models.CompanyUser.objects.filter(
            company_id=company_id,
            user=self.request.user.id,
        ).first()


class CompanyManagerRequiredMixin(CompanyUserRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        company = self.get_company()
        company_user = self.get_company_user(company)

        if not company_user:
            messages.add_message(
                request,
                messages.ERROR,
                type(self).permission_denied_message,
            )
            return redirect("homepage:homepage")

        if company_user.role != "manager":
            messages.add_message(
                request,
                messages.ERROR,
                _("You are not a manager in this company"),
            )
            return redirect(
                "workplace:tasks",
                company_id=self.kwargs.get("company_id"),
            )

        return super().dispatch(request, *args, **kwargs)
