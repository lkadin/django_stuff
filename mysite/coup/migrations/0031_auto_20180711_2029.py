# Generated by Django 2.0.4 on 2018-07-12 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coup', '0030_auto_20180711_2026'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='hand',
        ),
        migrations.AddField(
            model_name='player',
            name='hand',
            field=models.ManyToManyField(to='coup.CardInstance'),
        ),
    ]
