# Generated by Django 2.2.7 on 2020-01-28 09:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0027_auto_20200127_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='ssl',
            field=models.BooleanField(default=False, help_text='Сайт доступен по протоколу https://', verbose_name='SSL сертификат'),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='html',
            field=models.TextField(default='', verbose_name='HTML код'),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Site', verbose_name='Сайт'),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='title',
            field=models.CharField(default='Новый чанк', max_length=50, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='page',
            name='alias',
            field=models.CharField(default='', help_text='Для главной "/", для остальных без слэшей', max_length=100, verbose_name='Псевдоним'),
        ),
        migrations.AlterField(
            model_name='page',
            name='metadescription',
            field=models.TextField(default='', max_length=170, verbose_name='META-description'),
        ),
        migrations.AlterField(
            model_name='page',
            name='metatitle',
            field=models.CharField(default='', max_length=80, verbose_name='META-title'),
        ),
        migrations.AlterField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(blank=True, help_text='Макс. 3 уровня, пример: /first/second/third, родитель не указывается только у главной страницы, для остальных страниц 1 уровня родитель - Главная', null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Page', verbose_name='Родительская страница'),
        ),
        migrations.AlterField(
            model_name='page',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Site', verbose_name='Сайт'),
        ),
        migrations.AlterField(
            model_name='page',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Template', verbose_name='Шаблон'),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(default='Новая страница', max_length=100, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='placeholder',
            name='html',
            field=models.TextField(default='', verbose_name='HTML код'),
        ),
        migrations.AlterField(
            model_name='placeholder',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Page', verbose_name='Страница'),
        ),
        migrations.AlterField(
            model_name='placeholder',
            name='title',
            field=models.CharField(default='Новый плейсхолдер', max_length=50, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='placeholder',
            name='uniqenable',
            field=models.BooleanField(default=False, help_text='Включить уникализацию', verbose_name='Уникализация'),
        ),
        migrations.AlterField(
            model_name='region',
            name='address',
            field=models.CharField(default='', max_length=100, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='region',
            name='alias',
            field=models.CharField(default='', help_text='Например: "msk"', max_length=50, verbose_name='Псевдоним'),
        ),
        migrations.AlterField(
            model_name='region',
            name='email',
            field=models.CharField(default='', max_length=50, verbose_name='E-mail'),
        ),
        migrations.AlterField(
            model_name='region',
            name='main_region',
            field=models.BooleanField(default=False, help_text='Размещается на основном домене.', verbose_name='Основной регион'),
        ),
        migrations.AlterField(
            model_name='region',
            name='padeji',
            field=models.CharField(default='', help_text='Например: "Москва,Москвы,Москве,Москву,Москвой,Москве"', max_length=200, verbose_name='Наименование во всех падежах, через запятую'),
        ),
        migrations.AlterField(
            model_name='region',
            name='phone',
            field=models.CharField(default='', max_length=50, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='region',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Site', verbose_name='Сайт'),
        ),
        migrations.AlterField(
            model_name='region',
            name='title',
            field=models.CharField(default='Новый регион', max_length=50, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='site',
            name='build',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='site',
            name='domain',
            field=models.CharField(default='mysite.ru', max_length=50, verbose_name='Домен'),
        ),
        migrations.AlterField(
            model_name='site',
            name='ftp_host',
            field=models.CharField(default='', max_length=20, verbose_name='FTP хост'),
        ),
        migrations.AlterField(
            model_name='site',
            name='ftp_password',
            field=models.CharField(default='', max_length=30, verbose_name='FTP пароль'),
        ),
        migrations.AlterField(
            model_name='site',
            name='ftp_user',
            field=models.CharField(default='', max_length=30, verbose_name='FTP пользователь'),
        ),
        migrations.AlterField(
            model_name='site',
            name='robots',
            field=models.TextField(default='', help_text='Директивы HOST и SITEMAP не указываются, они проставляются автоматически.', verbose_name='Robots.txt'),
        ),
        migrations.AlterField(
            model_name='site',
            name='title',
            field=models.CharField(default='Новый сайт', max_length=50, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='template',
            name='html',
            field=models.TextField(default='', verbose_name='HTML код'),
        ),
        migrations.AlterField(
            model_name='template',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Site', verbose_name='Сайт'),
        ),
        migrations.AlterField(
            model_name='template',
            name='title',
            field=models.CharField(default='Новый шаблон', max_length=50, verbose_name='Наименование'),
        ),
    ]