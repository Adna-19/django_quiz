# Generated by Django 3.2 on 2021-04-27 12:19

from django.db import migrations
import quiz.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=quiz.fields.OrderField(blank=True, null=True),
        ),
    ]
