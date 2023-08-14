# Generated by Django 4.1.7 on 2023-08-14 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('live_class', '0013_alter_lessonplan_lesson_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterviewVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('embed_link', models.URLField()),
                ('lesson_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='live_class.lessonplan')),
            ],
        ),
    ]