from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import UserRegisterView, UserUpdateView, confirm_email

from . import views

app_name = UsersConfig.name


urlpatterns = [
    # Путь для регмстрации нового Порльзоввателя
    path("registration/", UserRegisterView.as_view(), name="registration"),
    # Прописываем путь для входа в Личный кабинет, переопределяем template_name
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    #  Путь для Выхода из Личного кабинетп
    path("logout/", LogoutView.as_view(), name="logout"),
    # Путь, по которому будет переходить Пользователь из своей почты на сайт,
    # при нажатии на сформированную для него ссылку
    path("confirm-register/<str:token>/", confirm_email, name="confirm_email"),
    # Путь для редактирования профиля Пользователя
    path("profile/", UserUpdateView.as_view(), name="profile"),
    # Путь для генерации нового пароля при Восстановлении пароля
    # path("profile/genpassword/", generate_new_password, name="generate_new_password"),
    # path("login/restore-password", restore_password, name="restore_password"),
    # Путь для обработки формы изменения пароля
    path(
        "password-change/", views.UserPasswordChange.as_view(), name="password-change"
    ),
    # Путь для отображения результата успешной смены паролч
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"),
        name="password-change-done",
    ),
    # Путь для перехода на страницу с вводом email, для отправки на него письма. Указываем template_name,
    # так как мы переопределяем его
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    # Путь для отображения результата отправки письма. Указываем template_name, так как мы переопределяем его
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"),
        name="password_reset_done",
    ),
    # Путь для формирования и отправки одноразоваго сообщения на почту
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    #  Путь для подтверждения смены пароля Пользователю
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]