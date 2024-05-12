from django import forms
from django.contrib.auth.forms import (PasswordChangeForm, UserChangeForm,
                                       UserCreationForm)

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Класс формы для создания нового объекта модели User"""

    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class UserForm(StyleFormMixin, UserChangeForm):
    """Класс формы для редактирования профиля Пользователя"""

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "phone_number",
            "country",
        ]

    def __init__(self, *args, **kwargs):
        """Метод для сокрытия поля password"""
        super().__init__(*args, **kwargs)

        self.fields["password"].widget = forms.HiddenInput()


class UserPasswordChangeForm(PasswordChangeForm):
    """Класс формы для формы смены пароля"""

    old_password = forms.CharField(
        label="Старый пароль", widget=forms.PasswordInput(attrs={"class": "form_input"})
    )
    new_password1 = forms.CharField(
        label="Новый пароль", widget=forms.PasswordInput(attrs={"class": "form_input"})
    )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form_input"}),
    )