# Generated by Django 3.1 on 2020-11-10 17:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0035_auto_20200414_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topvisor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.site', verbose_name='Сайт')),
            ],
            options={
                'verbose_name_plural': 'Топвизор',
            },
        ),
    ]