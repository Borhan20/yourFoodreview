# Generated by Django 4.1.7 on 2023-04-04 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_post_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_images',
            field=models.ImageField(default='', upload_to='media/post_images/'),
        ),
    ]
