from django.core.validators import RegexValidator
from api.managers import APIUserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from datetime import date

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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_staff = models.BooleanField(False)
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

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
 
class APIUserProfile(models.Model):
    user = models.OneToOneField(APIUser, on_delete=models.CASCADE, related_name='profile')
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phoneno = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    country_name = models.CharField(max_length=100)  # Store the name of the country
    state_name = models.CharField(max_length=100)  # Store the name of the state
    city_name = models.CharField(max_length=100)   # Store the name of the city
    address = models.TextField()
    zipcode = models.CharField(max_length=10)
    dateofbirth = models.DateField()

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
