from django.contrib import admin
from catalog.models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "is_published", "created_at")
    list_filter = ("is_published", "category",)
    search_fields = (
        "name",
        "description",
    )

    actions = ["publish", "unpublish"]

    def publish(self, request, queryset):
        queryset.update(is_published=True)
    publish.short_description = 'Опубликовать выбранные товары'

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
    unpublish.short_description = 'Снять с публикации выбранные товары'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")