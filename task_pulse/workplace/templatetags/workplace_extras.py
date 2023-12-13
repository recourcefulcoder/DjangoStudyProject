from django import template

from workplace import models

register = template.Library()


@register.simple_tag
def get_company_user(user, company_id):
    return models.CompanyUser.objects.filter(
        company_id=company_id,
        user=user,
    ).first()
