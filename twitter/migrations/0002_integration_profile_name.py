# Generated by Django 3.1 on 2020-09-09 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='integration',
            name='profile_name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
