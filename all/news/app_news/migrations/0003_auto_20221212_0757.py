# Generated by Django 2.2 on 2022-12-12 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0002_auto_20221212_0702'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
    ]
