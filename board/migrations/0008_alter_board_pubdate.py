# Generated by Django 4.0.3 on 2022-05-03 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_alter_board_pubdate_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 3, 10, 11, 53, 86361)),
        ),
    ]
