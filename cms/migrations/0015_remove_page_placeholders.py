# Generated by Django 2.2.7 on 2019-12-01 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0014_chunk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='placeholders',
        ),
    ]