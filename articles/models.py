from django.db import models

# Create your models here.


class Article(models.Model):
    name = models.CharField(max_length=300, verbose_name='название статьи')
    slug = models.CharField(max_length=300, verbose_name='slug', blank=True, null=True)
    text = models.TextField(blank=True, null=True, verbose_name='содержимое')
    preview = models.ImageField(upload_to='articles/', verbose_name='изображение', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='количество просмотров')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'
        ordering = ('name', )