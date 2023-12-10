from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from main.models import Log
# from api.task.models import Task

class AccessLevel:
    """
    Access Level for User Roles
    """
    CEO = 1000
    TEAM_MANAGER = 700
    SOFTWARE_ENGINEER = 300

    CEO_CODE = 'chief-executive-officer'
    TEAM_MANAGER_CODE = 'team-manager'
    SOFTWARE_ENGINEER_CODE = 'software-engineer'

    CHOICES = (
        (CEO, 'Chief Executive Officer'),
        (TEAM_MANAGER, 'Team Manager'),
        (SOFTWARE_ENGINEER, 'Software Engineer')
    )

    CODES = (
        (CEO, CEO_CODE),
        (TEAM_MANAGER, TEAM_MANAGER_CODE),
        (SOFTWARE_ENGINEER, SOFTWARE_ENGINEER_CODE)
    )

    DICT = dict(CHOICES)
    CODES_DICT = dict(CODES)

# Create your models here.
class Role(Log):
    """
    Role for User
    """
    name = models.CharField(db_column='Name', max_length=255, unique=True)
    code = models.SlugField(db_column='Code', default='')
    description = models.TextField(db_column='Description', null=True, blank=True)
    access_level = models.IntegerField(db_column='AccessLevel', choices=AccessLevel.CHOICES, default=AccessLevel.SOFTWARE_ENGINEER_CODE)

    class Meta:
        db_table = 'TaskTrackingRoles'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.code = slugify(self.name)
            super().save()
        except Exception:
            raise

    def getRoleByCode(self=None, code=None):
        try:
            return Role.objects.get(code__exact=code)
        except Exception as e:
            print(e)
            return e

class CustomUserManager(BaseUserManager):
    """
    Model Manger for our custom user model(inherits from BaseUserManager)
    """
    def create_user(self, email, password):
        user = self.model(email=email, password=password)
        pw = password
        user.set_password(pw)
        user.is_superuser = False
        user.is_approved = False
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        pw = password
        user.set_password(pw)
        user.is_superuser = True
        user.is_approved = True
        user.is_active = True
        user.role = Role.objects.get(code=AccessLevel.CEO_CODE)
        user.save()
        return user

class User(AbstractBaseUser, Log, PermissionsMixin):
    """
    User using Custom User Model(inherits from AbstractBaseUser)
    """
    first_name = models.CharField(db_column='FirstName',max_length=255, null=True)
    last_name = models.CharField(db_column='LastName',max_length=255, null=True)
    email = models.EmailField(unique=True, db_column='Email', default='')
    is_active = models.BooleanField(db_column='IsActive', default=True ,
                                    help_text='Designates whether this user should be treated as active')
    is_staff = models.BooleanField(db_column='IsStaff', default=True,
                                   help_text='Designates whether the user can log into this admin site')
    is_approved = models.BooleanField(db_column='IsApproved', default=False,
                                      help_text='Designates whether this user is approved or not')
    is_superuser = models.BooleanField(db_column='IsSuperUser', default=False,
                                      help_text='Designates whether this user is the superuser or not')
    role = models.ForeignKey(Role, db_column='RoleID', on_delete=models.CASCADE, default='', blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    class Meta:
        db_table ='Users'

    def __str__(self):
        return f'{self.first_name}'

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.email = self.email.replace(" ", "").lower()
            super().save()
        except Exception:
            raise
