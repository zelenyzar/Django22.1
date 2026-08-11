from django.db import models

class BlogPost(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок поста",
        help_text="Введите заголовок поста",
    )

    content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Содержимое",
        help_text="Введите текст вашего поста",
    )

    image = models.ImageField(
        upload_to="blog/previews/",
        blank=True,
        null=True,
        verbose_name="Превью (изображение)",
        help_text="Загрузите превью (изображение) поста",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано"
    )

    views_count = models.PositiveIntegerField(
        verbose_name='Количество просмотров',
        default=0
    )

    class Meta:
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

