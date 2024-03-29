# Generated by Django 2.2.7 on 2019-12-01 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0015_remove_page_placeholders'),
    ]

    operations = [
        migrations.CreateModel(
            name='Placeholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Новый плейсхолдер', max_length=50)),
                ('html', models.TextField(default='')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Page')),
            ],
            options={
                'verbose_name_plural': 'Плейсхолдеры',
            },
        ),
    ]
