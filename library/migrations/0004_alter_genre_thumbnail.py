# Generated by Django 4.2.15 on 2024-08-27 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_author_middle_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='thumbnail',
            field=models.ImageField(default='default/genre.png', upload_to='genre/'),
        ),
    ]
