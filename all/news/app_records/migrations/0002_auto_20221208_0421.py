# Generated by Django 2.2 on 2022-12-08 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_records', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recordimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='records/'),
        ),
    ]
