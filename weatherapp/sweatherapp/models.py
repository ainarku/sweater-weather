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

    def __str__(self):
        return f"{self.user.username}'s Preference: {self.temperature_unit}"


class WeatherData(models.Model):
    city_name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
        default=0.0
    )
    temperature_fahrenheit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
        default=0.0
    )
    feels_like = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=True
    )
    weather_description = models.TextField(
        max_length=255,
        blank=False,
        null=False,
        default="No Description"
    )
    humidity = models.CharField(
        max_length=5,
        blank=False,
        null=False)
    user_preference = models.ForeignKey(
        UserPreference,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["city_name"]

    def __str__(self):
        return (
            f"Weather in {self.city_name}: "
            f"{self.temperature}°C - "
            f"{self.temperature_fahrenheit}°F - "
            f"{self.weather_description}"
        )

    def humidity_percentage(self):
        return f"{self.humidity} %"


class ForecastData(models.Model):
    city_name = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    date_time = models.DateTimeField()
    temperature = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
        default=0.0
    )

    temperature_fahrenheit = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=False,
        default=0.0
    )
    feels_like = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=False,
        null=True
    )
    weather_description = models.TextField(
        max_length=255,
        blank=False,
        null=False,
        default="No Description"
    )
    humidity = models.CharField(
        max_length=5,
        blank=False,
        null=False
    )
    user_preference = models.ForeignKey(
        UserPreference,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return f"Forecast for {self.city_name} on {self.date_time}"

    def humidity_percentage(self):
        return f"{self.humidity} %"


class News(models.Model):
    title = models.CharField(
        max_length=255,
        blank=False,
        null=False
    )
    content = models.TextField(
        blank=False,
        null=False
    )
    image = models.ImageField(
        blank=True,
        null=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.title


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

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

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class FavouriteCity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)
    weather_data = models.OneToOneField(WeatherData, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "city_name")

    def __str__(self):
        return f"{self.user.username}'s favorite city: {self.city_name}"
