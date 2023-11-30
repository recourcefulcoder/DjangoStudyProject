from django.contrib.auth import hashers
from django.contrib.auth import models as auth_models
from django.core import mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def get_user_media_path(instance, filename):
    return f"""users/{instance.id}/profile_image.{filename.split(".")[-1]}"""


class UserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(
        self,
        email,
        first_name,
        last_name,
        password,
        **extra_fields,
    ):
        if not email:
            raise ValueError(_("The email must be set"))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.password = hashers.make_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email,
        first_name,
        last_name,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email,
            first_name,
            last_name,
            password,
            **extra_fields,
        )

    def create_superuser(
        self,
        first_name,
        last_name,
        email=None,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(
            email,
            first_name,
            last_name,
            password,
            **extra_fields,
        )


class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site.",
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts.",
        ),
    )
    email = models.EmailField(
        _("email address"),
        help_text=_("Enter your valid email address."),
        unique=True,
    )
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    image = models.ImageField(
        _("profile image"),
        upload_to=get_user_media_path,
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        mail.send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
