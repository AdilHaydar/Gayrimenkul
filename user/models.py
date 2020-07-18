from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.core.validators import RegexValidator
# Create your models here.


USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

class UserManager(BaseUserManager):
    def create_user(self,username,is_telefonu, email,registration_code=None,cep_telefonu=None,full_name=None, password=None, active=True, is_staff = False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            username = username,
            email = self.normalize_email(email),
            full_name = full_name,
            registration_code=registration_code,
            cep_telefonu=cep_telefonu,
            is_telefonu=is_telefonu
        )
        if not username:
            raise ValueError('Users must have a username')
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = active
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,cep_telefonu="None",is_telefonu="none",full_name=None,registration_code='None', password=None):
        cep_telefonu = input("Cep Telefonu : ") 
        user = self.create_user(
            username,cep_telefonu=cep_telefonu,email=email,is_telefonu=is_telefonu,full_name=full_name,registration_code=registration_code, password = password
           
            ,is_admin=True, is_staff=True
        )
        user.save(using=self._db)
        return user
    def create_staffuser(self,email,password=None):
        user = self.create_user(
            email,password=password,is_staff=True
        )
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length = 30,
    unique=True,
    verbose_name = "Username",
    validators = [RegexValidator(regex = USERNAME_REGEX,
    message="Username must be alphanumeric or contain numbers",
    code="invalid_username")])
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name = "Email",
    )
    cep_telefonu = models.CharField(unique=True,max_length=20,blank=False,null=False, verbose_name="Cep Telefonu")
    is_telefonu = models.CharField(max_length=20,blank=True, null=True, verbose_name="İş Telefonu")
    registration_code = models.CharField(max_length=20,blank=False)
    full_name = models.CharField(max_length=30, blank=True, null=True,verbose_name = "Ad Soyad")
    active = models.BooleanField(default = True)
    staff = models.BooleanField(default = False)
    admin = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "username" 
    REQUIRED_FIELDS = ["email"]
    def __str__(self):
        return self.username

    def get_short_name(self):
        pass

    @property
    def is_staff(self):
        return self.staff
    @property
    def is_admin(self):
        return self.admin
    @property
    def is_active(self):
        return self.active

    def has_perm(self, perm, obj=None):
       return self.admin

    def has_module_perms(self, app_label):
       return self.admin
    



class UserUpdateModel(models.Model):
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name = "Email",
    )
    
    full_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Ad Soyad")
    cep_telefonu = models.CharField(max_length=20,blank=False,null=False, verbose_name="Cep Telefonu",unique=True)
    is_telefonu = models.CharField(max_length=20,blank=True, null=True, verbose_name="İş Telefonu")