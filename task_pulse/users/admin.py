from django.contrib import admin

from users import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = [
        models.User.first_name.field.name,
        models.User.last_name.field.name,
        models.User.email.field.name,
        models.User.password.field.name,
    ]
