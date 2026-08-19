import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Создаёт нового уникального тестового пользователя (вход по email) при каждом запуске."

    def handle(self, *args, **options):
        timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
        rand = random.randint(1000, 9999)
        email = f"test-{timestamp}-{rand}@example.com"
        password = "TestPass123!"

        user = User.objects.create(
            email=email,
            first_name="Тестовый",
            last_name="Пользователь",
            is_active=True,
            is_staff=False,
        )

        user.set_password(password)
        user.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Создан новый пользователь:\n"
                f"   Email (логин): {email}\n"
                f"   Пароль: {password}\n"
                f"   ID: {user.id}"
            )
        )
