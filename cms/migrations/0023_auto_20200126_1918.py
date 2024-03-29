# Generated by Django 2.2.7 on 2020-01-26 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0022_placeholder_uniqenable'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='log',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='page',
            name='alias',
            field=models.CharField(default='', help_text='Для главной "/", для остальных без слэшей', max_length=100),
        ),
        migrations.AlterField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Макс. 3 уровня, пример: /first/second/third, родитель не указывается только у главной страницы, для остальных страниц 1 уровня родитель - Главная', null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Page'),
        ),
        migrations.AlterField(
            model_name='region',
            name='alias',
            field=models.CharField(default='', help_text='Например: "msk"', max_length=50),
        ),
        migrations.AlterField(
            model_name='region',
            name='padeji',
            field=models.CharField(default='', help_text='Например: "Москва,Москвы,Москве,Москву,Москвой,Москве"', max_length=200),
        ),
    ]
