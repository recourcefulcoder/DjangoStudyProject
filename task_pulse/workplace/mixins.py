from django.contrib.auth import mixins
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from workplace import models


class CompanyUserRequiredMixin(mixins.UserPassesTestMixin):
    permission_denied_message = _("You are not a participant in this company")

    def test_func(self, roles=["employee", "owner", "manager"]):
        company = self.get_company()
        company_user = self.get_company_user(company.id)

        if not company_user:
            return False

        if company_user.role not in roles:
            return False

        return True

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
    def get_test_func(self):
        def new_func():
            return self.test_func(roles=["manager", "owner"])

        return new_func


class CompanyOwnerRequiredMixin(CompanyUserRequiredMixin):
    def get_test_func(self):
        def new_func():
            return self.test_func(roles=["owner"])

        return new_func
