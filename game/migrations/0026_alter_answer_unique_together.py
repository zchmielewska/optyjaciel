# Generated by Django 3.2.8 on 2021-10-29 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_rename_option0_questionset_option4'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer',
            unique_together={('user', 'quiz_item')},
        ),
    ]