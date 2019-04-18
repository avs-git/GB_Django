# Generated by Django 2.1.7 on 2019-04-17 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nesting_level', models.IntegerField()),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='имя')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('image_preview', models.ImageField(blank=True, upload_to='products_images/preview', verbose_name='Картинка категории. Preview')),
                ('image', models.ImageField(blank=True, upload_to='products_images/preview', verbose_name='Картинка категории')),
                ('is_active', models.BooleanField(default=True, verbose_name='активна')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='nested_category', to='mainapp.Category')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
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
                ('SKU', models.CharField(blank=True, max_length=25, verbose_name='Артикул')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='количество на складе')),
                ('is_active', models.BooleanField(default=True, verbose_name='активно')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='имя подкатегории')),
                ('description', models.TextField(blank=True, verbose_name='описание подкатегории')),
                ('image_preview', models.ImageField(blank=True, upload_to='products_images/preview', verbose_name='Preview/ подкатегории')),
                ('image', models.ImageField(blank=True, upload_to='products_images/preview', verbose_name='Картинка подкатегории')),
                ('is_active', models.BooleanField(default=True, verbose_name='активна')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Category')),
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.SubCategory'),
        ),
    ]
