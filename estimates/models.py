import os

from django.core.exceptions import ValidationError
from django.db import models


def validate_gge_extension(value):
    ext = os.path.splitext(value.name)[-1]  # Получаем расширение файла
    if not ext.lower() == '.gge':
        raise ValidationError('Допускаются только файлы формата .gge')


class Estimate(models.Model):
    # Статусы для наглядности
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('processing', 'В обработке'),
        ('checked', 'Проверена'),
        ('error', 'Ошибка'),
    ]

    title = models.CharField("Название сметы", max_length=255)
    file = models.FileField(
        "Файл .gge",
        upload_to='estimates/',
        validators=[validate_gge_extension] # Добавляем проверку здесь
    )
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField("Дата загрузки", auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"

    class Meta:
        verbose_name = "Смета"
        verbose_name_plural = "Сметы"

