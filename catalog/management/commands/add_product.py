from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **options):
        self.stdout.write('Очистка данных...')
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Данные очищены'))

        category, _ = Category.objects.get_or_create(name='Чупачупс', description='чупачупс')

        products = [
            {'name': 'Чупакабра', 'description': 'что-то', 'category': category, 'price': '999'},
            {'name': 'Чупакабра1', 'description': 'что-то', 'category': category, 'price': '9991'}
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Продукт добавлен: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Продукт уже существует: {product.name}'))

        call_command('loaddata', 'foodstuff.json')
        self.stdout.write(self.style.SUCCESS('Успешная загрузка данных из фикстур'))