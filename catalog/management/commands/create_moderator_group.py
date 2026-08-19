from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        unpublish_perm = Permission.objects.filter(
            content_type=content_type, codename="can_unpublish_product"
        ).first()

        delete_perm = Permission.objects.get(
            content_type=content_type, codename="delete_product"
        )

        if not unpublish_perm:
            self.stdout.write(self.style.ERROR("Разрешение can_unpublish_product не найдено. Проверьте миграции."))
            return

        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        group.permissions.add(unpublish_perm, delete_perm)

        self.stdout.write(
            self.style.SUCCESS(f"Группа 'Модератор продуктов' {'создана' if created else 'обновлена'}.")
        )
