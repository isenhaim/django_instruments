# Generated by Django 3.0.4 on 2020-11-01 08:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0019_auto_20201028_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 2, 8, 51, 58, 641409, tzinfo=utc)),
        ),
    ]
