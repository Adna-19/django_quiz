# Generated by Django 3.2 on 2021-04-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20210428_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='ends_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='starts_at',
            field=models.DateTimeField(),
        ),
    ]
