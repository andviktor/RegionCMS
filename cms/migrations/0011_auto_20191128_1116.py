# Generated by Django 2.2.7 on 2019-11-28 11:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='template',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cms.Template'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.Page'),
        ),
    ]
