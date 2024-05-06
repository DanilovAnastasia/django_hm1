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
    photo = models.ImageField(upload_to='product/', **NULLABLE, verbose_name='изображение(превью)')
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Version(models.Model):
    """Модель для версии продукта"""
    # related_name говорит об отношении один ко многим (у одного продукта м.б. несколько версий).
    # М.Б. обращаться как product.versions, а не product.version_set
    product = models.ForeignKey(Product, related_name='versions', verbose_name='Продукт', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(verbose_name=' Номер версии', blank=True, null=True)
    name = models.CharField(max_length=150, verbose_name='Название версии')
    is_current = models.BooleanField(default=True, verbose_name='Признак актуальности')

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ('name',)

    def __str__(self):
        return self.name
