# Generated by Django 3.2.8 on 2021-11-02 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0027_alter_match_matched_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=256)),
                ('option1', models.CharField(max_length=256)),
                ('option2', models.CharField(max_length=256)),
                ('option3', models.CharField(max_length=256)),
                ('option4', models.CharField(max_length=256)),
                ('suggested_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.user')),
            ],
        ),
    ]