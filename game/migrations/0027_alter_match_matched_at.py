# Generated by Django 3.2.8 on 2021-11-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_alter_answer_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='matched_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]