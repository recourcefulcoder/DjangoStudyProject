from django.contrib.auth import mixins
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from workplace import models


class GiveCompanyUserToContext:
    # must (!!!) be put to the first place in inheritance list
    # in order to let super() access proper get_context_data method
    def get_context_data(self, **kwargs):
        context = super(GiveCompanyUserToContext, self).get_context_data(
            **kwargs,
        )
        context["company_user"] = models.CompanyUser.objects.filter(
            company_id=self.request.resolver_match.kwargs["company_id"],
            user=self.request.user,
        ).first()
        return context


class BaseCompanyUserRequiredMixin(mixins.UserPassesTestMixin):
    permission_denied_message = _("You dont have permission to this page")

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
        return models.CompanyUser.objects.get(
            company_id=company_id,
            user=self.request.user.id,
        )


class CompanyUserRequiredMixin(
    GiveCompanyUserToContext,
    BaseCompanyUserRequiredMixin,
):
    pass


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
