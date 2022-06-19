# Generated by Django 2.2.16 on 2022-06-16 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(null=True),
        ),
    ]