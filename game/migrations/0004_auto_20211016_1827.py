# Generated by Django 3.2.8 on 2021-10-16 16:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20211016_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet10',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet10', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet3',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet3', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet4',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet4', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet5',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet5', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet6',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet6', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet7',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet7', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet8',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet8', to='game.questionset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='quiz',
            name='QuestionSet9',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='QuestionSet9', to='game.questionset'),
            preserve_default=False,
        ),
    ]