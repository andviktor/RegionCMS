# Generated by Django 2.2.7 on 2020-01-26 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0025_auto_20200126_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='upload_date',
            field=models.CharField(default='', max_length=30),
        ),
    ]
