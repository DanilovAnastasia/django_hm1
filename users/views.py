import secrets

from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import (UserForm, UserPasswordChangeForm,
                         UserRegisterForm)
from users.models import User


class UserRegisterView(CreateView):
    """Класс для создания нового Пользователя"""

    model = User
    form_class = UserRegisterForm

    def get_success_url(self):
        """Метод для определения пути, куда будет совершен переход после создания Пользователя"""

        # reverse только получает нужный url
        return reverse("users:login")

    def form_valid(self, form):
        """Метод верифекации email"""
        # Формируем токен
        token = secrets.token_hex(16)
        # Вызываем user и сохраняем его форму
        user = form.save()
        # Вызываем токен
        user.token = token
        # После регистрации, пока ещё нет подтверждение почты, зайти на сайт не сможет.
        # Функция confirm_email будет его активировать
        user.is_active = False
        user.save()
        # Функция get_host() получает host, с которого пришел пользователь
        host = self.request.get_host()
        # confirm_register - точка входа, users - указано в путях (config urls.py) в переходе к Приложению users
        # Данный сформировавнный link будет отправлен Пользователю. При его нажатии он попадет
        link = f"http://{host}/users/confirm-register/{token}"
        # Формируем отправление письма на почту
        message = f"Вы успешно зарегистрировались на сайте 'Здоровье в ложке'. Предлагаем Вам подтвердить почту {link}"
        # Настраиваем отправление письма, копируем данню строку с сайта https://vivazzi.pro/ru/it/send-email-in-django/
        send_mail("Верификация почты", message, settings.EMAIL_HOST_USER, [user.email])

        return super().form_valid(form)


def confirm_email(request, token):
    """Функция по токену получает Пользователя (user), проверяет наличие токена и регистрайии.
    По итогу выдает ошибку 404 или сохраняет Польхователя"""
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    # Будет перенаправлять на страницу с формой для Входа на сайт
    # При этом reverse только получает нужный url, а redirect уже перенаправляет
    return redirect(reverse("users:login"))


class UserUpdateView(UpdateView):
    """Класс для редактирования профиля Пользователя"""

    model = User
    success_url = reverse_lazy("users:profile")
    form_class = UserForm

    def get_object(self, queryset=None):
        """
        Метод, получающий объект для редактирования.
        Нужен здесб как вариант, чтобы не использовать 'pk' в urls.py
        """
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    """Класс для переопределения PasswordChangeView"""

    form_class = UserPasswordChangeForm
    template_name = "users/password_change_form.html"
    success_url = reverse_lazy("users:password-change-done")