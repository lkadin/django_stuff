# Generated by Django 2.0.4 on 2018-07-10 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coup', '0020_auto_20180710_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardinstance',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
