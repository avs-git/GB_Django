# Generated by Django 2.1.7 on 2019-03-31 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='имя продукта')),
                ('image', models.ImageField(blank=True, upload_to='products_images', verbose_name='Изображение товара')),
                ('image_preview', models.ImageField(blank=True, upload_to='products_images/preview', verbose_name='Preview')),
                ('short_desc', models.CharField(blank=True, max_length=60, verbose_name='краткое описание продукта')),
                ('description', models.TextField(blank=True, verbose_name='описание продукта')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='цена продукта')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='количество на складе')),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='имя')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='имя подкатегории')),
                ('description', models.TextField(blank=True, verbose_name='описание продукта')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ProductCategory')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.SubCategory'),
        ),
    ]
