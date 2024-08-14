from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, phone,email,first_name,last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not phone:
            raise ValueError("Users must have an phone number")

        user = self.model(
            phone=phone,
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,phone,email=None,first_name=None,last_name=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            phone=phone,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone = models.CharField(max_length=11 , unique=True , verbose_name="phone number")
    email = models.EmailField(verbose_name="email address",max_length=255,)
    first_name = models.CharField(verbose_name="first name", max_length=30, blank=True)
    last_name = models.CharField(verbose_name="last name", max_length=30, blank=True)
    biography = models.CharField(verbose_name="biography", max_length=300, blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ['email','first_name','last_name']

    def __str__(self):
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
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Otp(models.Model):
    phone = models.CharField(max_length=11)
    code = models.CharField(max_length=4)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.phone}  =  {self.code}'


class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    first_name = models.CharField(max_length=11)
    last_name = models.CharField(max_length=11)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    postal_code = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    username = models.CharField(max_length=11)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.username




