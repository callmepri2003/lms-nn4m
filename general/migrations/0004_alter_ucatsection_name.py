# Generated by Django 4.1.7 on 2023-02-17 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_ucatsectioninstance_skills_mastered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucatsection',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
