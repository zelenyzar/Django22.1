from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Product)

        change_perm = Permission.objects.get(
            content_type=content_type, codename="change_product"
        )
        view_perm = Permission.objects.get(
            content_type=content_type, codename="view_product"
        )
        add_perm = Permission.objects.get(
            content_type=content_type, codename="add_product"
        )
        delete_perm = Permission.objects.get(
            content_type=content_type, codename="delete_product"
        )

        managers, _ = Group.objects.get_or_create(name="Managers")
        editors, _ = Group.objects.get_or_create(name="Editors")

        managers.permissions.add(change_perm, view_perm, add_perm, delete_perm)
        editors.permissions.add(view_perm, change_perm)

        self.stdout.write(self.style.SUCCESS("Группы и права успешно созданы."))
