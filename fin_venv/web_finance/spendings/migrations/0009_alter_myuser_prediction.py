# Generated by Django 4.1.6 on 2023-03-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spendings', '0008_alter_myuser_prediction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='prediction',
            field=models.JSONField(default={'categories': [], 'day_prediction': [], 'month_prediction': []}),
        ),
    ]
