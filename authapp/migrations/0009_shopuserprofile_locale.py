# Generated by Django 2.1.7 on 2019-05-03 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_auto_20190503_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopuserprofile',
            name='locale',
            field=models.CharField(blank=True, max_length=128, verbose_name='Страна/язык'),
        ),
    ]
