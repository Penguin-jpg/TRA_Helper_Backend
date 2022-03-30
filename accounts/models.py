from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied


class TRAUserManager(BaseUserManager):
    use_in_migrations = True

    def get_by_natural_key(self, identity_number):
        return self.get(**{self.model.USERNAME_FIELD: identity_number})

    def _create_user(self, identity_number, email, password, **extra_fields):
        """
        透過身分證字號、email、密碼來建立使用者
        """
        if not identity_number:
            raise ValueError("必須要有身分證字號")

        email = self.normalize_email(email)
        user = self.model(identity_number=identity_number, email=email, **extra_fields)
        user.password = make_password(password)
        print(user.password)
        user.save(using=self._db)
        return user

    def create_user(self, identity_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(identity_number, email, password, **extra_fields)

    def create_superuser(
        self, identity_number, email=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(identity_number, email, password, **extra_fields)

    def with_perm(
        self, perm, is_active=True, include_superusers=True, backend=None, obj=None
    ):
        if backend is None:
            backends = auth._get_backends(return_tuples=True)
            if len(backends) == 1:
                backend, _ = backends[0]
            else:
                raise ValueError(
                    "You have multiple authentication backends configured and "
                    "therefore must provide the `backend` argument."
                )
        elif not isinstance(backend, str):
            raise TypeError(
                "backend must be a dotted import path string (got %r)." % backend
            )
        else:
            backend = auth.load_backend(backend)
        if hasattr(backend, "with_perm"):
            return backend.with_perm(
                perm,
                is_active=is_active,
                include_superusers=include_superusers,
                obj=obj,
            )
        return self.none()

    def _user_has_perm(user, perm, obj):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_perm"):
                continue
            try:
                if backend.has_perm(user, perm, obj):
                    return True
            except PermissionDenied:
                return False
        return False

    def _user_has_module_perms(user, app_label):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        for backend in auth.get_backends():
            if not hasattr(backend, "has_module_perms"):
                continue
            try:
                if backend.has_module_perms(user, app_label):
                    return True
            except PermissionDenied:
                return False
        return False


# 會員
class TRAUser(AbstractBaseUser, PermissionsMixin):
    objects = TRAUserManager()
    identity_number = models.CharField(
        max_length=10, blank=False, unique=True, verbose_name="身分證字號"
    )  # 當做帳號
    password = models.CharField(max_length=128, blank=False, verbose_name="密碼")
    email = models.EmailField(blank=False, verbose_name="電子信箱")
    first_name = models.CharField(max_length=10, verbose_name="名稱")
    last_name = models.CharField(max_length=10, verbose_name="姓氏")
    phone_number = models.CharField(max_length=10, verbose_name="手機號碼")
    is_visually_impaired = models.BooleanField(default=False, verbose_name="視障人士")

    USERNAME_FIELD = "identity_number"  # 使用身分證字號登入
    REQUIRED_FIELDS = ["password", "email"]

    class Meta:
        verbose_name = "TRA_user"
        verbose_name_plural = "TRA_users"

    def get_full_name(self):
        """
        回傳全名
        """
        return self.last_name + self.first_name
