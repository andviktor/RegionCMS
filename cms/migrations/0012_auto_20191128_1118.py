# Generated by Django 2.2.7 on 2019-11-28 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0011_auto_20191128_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Page'),
        ),
    ]
