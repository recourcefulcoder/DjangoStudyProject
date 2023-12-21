from django.contrib import admin

from workplace import models


admin.site.register(models.Task)
admin.site.register(models.Company)
admin.site.register(models.CompanyUser)
