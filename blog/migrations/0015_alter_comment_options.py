# Generated by Django 3.2.12 on 2023-05-11 23:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_comment_parent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_added']},
        ),
    ]