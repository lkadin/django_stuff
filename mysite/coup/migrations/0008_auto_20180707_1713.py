# Generated by Django 2.0.4 on 2018-07-07 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coup', '0007_player_coins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='coins',
            field=models.IntegerField(default=2),
        ),
    ]
