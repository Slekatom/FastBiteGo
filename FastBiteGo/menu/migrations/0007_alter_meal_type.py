# Generated by Django 5.2.1 on 2025-06-07 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_meal_progress_stock_alter_meal_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meal',
            name='type',
            field=models.CharField(choices=[('Default', 'Default'), ('New', 'New'), ('Trending', 'Trending')], default='Default', max_length=30),
        ),
    ]
