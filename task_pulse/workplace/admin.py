from django.contrib import admin

from workplace import models as wp_models

admin.site.register(wp_models.CompanyUser)
admin.site.register(wp_models.Company)
