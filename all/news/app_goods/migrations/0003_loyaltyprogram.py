# Generated by Django 2.2 on 2022-12-12 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0002_auto_20221212_0751'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoyaltyProgram',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
            ],
        ),
    ]