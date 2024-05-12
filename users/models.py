from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель для Пользователя"""

    # Прописываам данную информацию, так как будем менять на emaıl
    username = None

    avatar = models.ImageField(
        upload_to="users_avatar",
        verbose_name="Аватар пользователя",
        help_text="Загрузите изображение",
        **NULLABLE
    )
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона",
        help_text="Укажите Ваш номер телефона",
        blank=True,
        null=True,
    )
    country = models.CharField(
        max_length=100,
        verbose_name="Страна",
        help_text="Введите страну проживания",
        **NULLABLE
    )
    email = models.EmailField(
        max_length=100,
        verbose_name="email",
        unique=True,
        help_text="Введите emaıl",
    )
    token = models.CharField(
        max_length=50,
        verbose_name="Токен",
        blank=True,
        null=True,
    )

    # Выбираем полем для авторизации email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользоаптель"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email