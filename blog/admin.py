from django.contrib import admin
from blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "content")
    list_filter = ("created_at",)
    search_fields = (
        "title",
    )