# Generated by Django 4.1.7 on 2023-04-04 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_images',
            field=models.ImageField(default='default.jpg', upload_to='post_images/'),
        ),
    ]
