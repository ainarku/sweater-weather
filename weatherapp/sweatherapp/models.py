from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.db import models
from django.conf import settings


class UserPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    temperature_unit = models.CharField(
        max_length=1,
        choices=[('C', 'Celsius'), ('F', 'Fahrenheit')],
        default=settings.DEFAULT_TEMPERATURE_UNIT
    )


class WeatherData(models.Model):
    city_name = models.CharField(max_length=255,
                                 blank=False,
                                 null=False
                                 )
    temperature = models.DecimalField(max_digits=5,
                                      decimal_places=2,
                                      blank=False,
                                      null=False
                                      )
    temperature_fahrenheit = models.DecimalField(max_digits=5,
                                                 decimal_places=2,
                                                 blank=False,
                                                 null=False
                                                 )
    feels_like = models.DecimalField(max_digits=5,
                                     decimal_places=2,
                                     blank=False,
                                     null=True
                                     )
    weather_description = models.CharField(max_length=255,
                                           blank=False,
                                           null=False)
    humidity = models.IntegerField(blank=False,
                                   null=False
                                   )
    user_preference = models.ForeignKey(UserPreference,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        blank=True
                                        )

    def __str__(self):
        return (
            f"Weather in {self.city_name}: "
            f"{self.temperature}°C - "
            f"{self.temperature_fahrenheit}°F - "
            f"{self.weather_description}"
        )


class News(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    content = models.TextField(blank=False, null=False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30,
        unique=True,
        default="",
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
