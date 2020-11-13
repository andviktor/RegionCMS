# Generated by Django 3.1 on 2020-11-13 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0037_auto_20201110_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='topvisor',
            name='scheduleday',
            field=models.CharField(default='', help_text='ALL - каждый день; YANDEX_UPDATE - после апдейтов Яндекса; AFTER_CHECK - после проверки; MONDAY - понедельник; TUESDAY - вторник; WEDNESDAY - среда; THURSDAY - четверг; FRIDAY - пятница; SATURDAY - суббота; SUNDAY - воскресенье; 0..27 - день месяца (число от 1 до 27); LAST_OF_MONTH - последний день месяца', max_length=10, verbose_name='День проверки'),
        ),
        migrations.AddField(
            model_name='topvisor',
            name='schedulehour',
            field=models.CharField(default='', help_text='1-24', max_length=50, verbose_name='Час проверки'),
        ),
    ]
