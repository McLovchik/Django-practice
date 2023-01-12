# Generated by Django 2.2 on 2022-12-12 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0003_loyaltyprogram'),
        ('app_users', '0002_auto_20221212_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='loyalty_program_item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_goods.LoyaltyProgram', verbose_name='loyalty program item'),
        ),
    ]