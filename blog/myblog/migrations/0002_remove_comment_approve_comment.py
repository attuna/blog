# Generated by Django 4.0.4 on 2022-05-26 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='approve_comment',
        ),
    ]
