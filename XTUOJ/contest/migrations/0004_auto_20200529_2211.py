# Generated by Django 3.0.3 on 2020-05-29 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0003_auto_20200529_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oicontestrank',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='oicontestrank',
            name='total_score',
            field=models.IntegerField(default=0),
        ),
    ]
