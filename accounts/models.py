from datetime import date

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.forms import DateTimeField


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Bruker må ha en e-postadresse")
        if not password:
            raise ValueError("Bruker må ha et passord")
        if not first_name:
            raise ValueError("empty first_name")
        if not last_name:
            raise ValueError("empty last_name")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
        )
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    picture = models.ImageField(upload_to="images/users", blank=True)
    phone = models.CharField(max_length=50, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    personal_number = models.IntegerField(null=True)
    account_number = models.IntegerField(null=True)
    is_active = models.BooleanField(default=True)  # can login
    admin = models.BooleanField(default=False)  # can login
    staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.birthdate and self.birthdate > date.today():
            raise ValidationError("The date cannot be in the future!")
        super(User, self).save(*args, **kwargs)

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def full_name(self):
        "Is the user full name"
        return f"{self.first_name} {self.last_name}"

    @property
    def is_staff(self):
        "Is the user a admin member?"
        return self.staff
