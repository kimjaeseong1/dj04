# Generated by Django 4.0.3 on 2022-04-26 23:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_rename_subjects_board_subject_alter_board_pubdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='pubdate',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 26, 23, 10, 11, 505584)),
        ),
    ]
