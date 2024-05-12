from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Класс для создания superuser, он нужен когда сломалась работа createsuperuser после нашего переопределения
    в модели User username"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@sky.pro",
            # Поля, которые разрешат вход в Админку
            is_staff=True,
            is_superuser=True,
        )
        # Функция set_password() нужна для кеширования пароля
        user.set_password("123qwe")
        # Функцмя save() нужна для сохранения пользователя
        user.save()

        print(f"Создание superuser  прошло успешно: {user.email} пароль: 123qwe")