# Generated by Django 5.2.1 on 2025-05-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
