# Generated by Django 2.0.4 on 2018-08-19 22:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('coup', '0027_auto_20180819_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='description',
            field=models.CharField(default=models.CharField(default='Assassinate', max_length=20), max_length=20),
        ),
    ]