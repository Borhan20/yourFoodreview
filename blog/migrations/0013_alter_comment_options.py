# Generated by Django 3.2.12 on 2023-05-07 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['date_added']},
        ),
    ]
