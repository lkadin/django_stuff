# Generated by Django 2.0.4 on 2018-07-07 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coup', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('playerName', models.CharField(default='Lee', max_length=20)),
            ],
        ),
    ]