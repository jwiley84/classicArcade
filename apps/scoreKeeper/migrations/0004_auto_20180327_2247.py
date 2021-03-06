# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-27 22:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_reg', '0001_initial'),
        ('scoreKeeper', '0003_game_gamer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalScore', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='game',
            old_name='gameTitle',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='game',
            name='gamer',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player',
        ),
        migrations.RemoveField(
            model_name='game',
            name='total_score',
        ),
        migrations.AddField(
            model_name='score',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gameScores', to='scoreKeeper.Game'),
        ),
        migrations.AddField(
            model_name='score',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playerScores', to='login_reg.User'),
        ),
    ]
