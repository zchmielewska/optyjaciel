# Generated by Django 3.2.8 on 2021-10-16 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='QuestionSet1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet1', to='game.questionset'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='QuestionSet2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet2', to='game.questionset'),
        ),
    ]