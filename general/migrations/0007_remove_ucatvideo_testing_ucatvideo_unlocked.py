# Generated by Django 4.1.7 on 2023-02-17 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0006_ucatvideo_testing'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ucatvideo',
            name='testing',
        ),
        migrations.AddField(
            model_name='ucatvideo',
            name='unlocked',
            field=models.BooleanField(default=False),
        ),
    ]
