# Generated by Django 4.1.7 on 2023-04-05 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_post_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_images',
            field=models.ImageField(default='pizza.jpg', upload_to='post_images'),
        ),
    ]
