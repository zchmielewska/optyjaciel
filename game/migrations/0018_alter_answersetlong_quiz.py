# Generated by Django 3.2.8 on 2021-10-28 20:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20211028_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersetlong',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.quizlong'),
        ),
    ]
