# Generated by Django 5.0.3 on 2024-04-21 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='product/', verbose_name='изображение(превью)'),
        ),
    ]
