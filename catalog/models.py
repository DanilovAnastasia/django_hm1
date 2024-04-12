from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(verbose_name='наименование')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    # created_at = models.CharField(max_length=150, verbose_name='вносимое поле')

    def __str__(self):
        return f'{self.name} ({self.description})'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(**NULLABLE, verbose_name='описание')
    price = models.PositiveIntegerField(default=0, verbose_name='цена за покупку')
    photo = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='изображение(превью)')
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

# Create your models here.
