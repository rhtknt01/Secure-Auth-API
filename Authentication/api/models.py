from django.utils import timezone
from django.core.validators import RegexValidator
from api.managers import APIUserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from datetime import date, timedelta

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    phone_code = models.CharField(max_length=10)
    nationality = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

class APIUser(AbstractBaseUser):
    email = models.CharField(verbose_name="email address", max_length=255, unique=True)
    user_id = models.CharField(max_length=12, unique=True, editable=False)  # New field for user ID
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    objects = APIUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
 
class APIUserProfile(models.Model):
    user = models.OneToOneField(APIUser, on_delete=models.CASCADE, related_name='profile')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phoneno = models.CharField(
        blank=False,
        null=False,
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    country_name = models.CharField(max_length=100, blank=False, null=False)  # Store the name of the country
    state_name = models.CharField(max_length=100, blank=False, null=False)  # Store the name of the state
    city_name = models.CharField(max_length=100, blank=False, null=False)   # Store the name of the city
    address = models.TextField()
    zipcode = models.CharField(max_length=10, blank=False, null=False)
    dateofbirth = models.DateField()
    profile_status = models.BooleanField(default=False, null=False)

    def __str__(self):
        return f'{self.firstname} {self.lastname} - {self.user.email}'

    class Meta:
        verbose_name = 'API User Profile'
        verbose_name_plural = 'API User Profiles'
        unique_together = ('user', 'phoneno')

    @property
    def full_name(self):
        return f'{self.firstname} {self.lastname}'

    @property
    def location(self):
        return f'{self.city.name}, {self.state.name}, {self.country.name}'

    @property
    def age(self):
        today = date.today()
        age = today.year - self.dateofbirth.year
        if today.month < self.dateofbirth.month or (today.month == self.dateofbirth.month and today.day < self.dateofbirth.day):
            age -= 1
        return age



class RefreshToken(models.Model):
    user = models.ForeignKey(APIUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=512, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expired_at:
            self.expired_at = timezone.now() + timedelta(days=30)
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.revoked and timezone.now() < self.expired_at

    def __str__(self):
        return f"{self.user.email} - {self.token}"
    
class BlackListedToken(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blacklisted_at