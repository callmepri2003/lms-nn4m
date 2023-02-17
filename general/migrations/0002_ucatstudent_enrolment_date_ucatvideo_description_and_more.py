# Generated by Django 4.1.7 on 2023-02-17 01:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucatstudent',
            name='enrolment_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 17, 12, 40, 0, 248479)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ucatvideo',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ucatvideo',
            name='name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
