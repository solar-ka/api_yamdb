# Generated by Django 2.2.16 on 2022-06-20 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.SlugField(choices=[('user', 'юзер'), ('moderator', 'модератор'), ('admin', 'администратор'), ('superuser', 'суперюзер')], default='user', max_length=16, verbose_name='роль'),
        ),
    ]
