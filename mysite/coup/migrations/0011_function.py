# Generated by Django 2.0.4 on 2018-07-28 23:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('coup', '0010_action_player2_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('methodName', models.CharField(blank=True, max_length=20, null=True)),
                ('arguments', models.TextField()),
            ],
        ),
    ]
