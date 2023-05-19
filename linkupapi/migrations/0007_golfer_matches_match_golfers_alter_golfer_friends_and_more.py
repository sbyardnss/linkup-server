# Generated by Django 4.2.1 on 2023-05-19 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('linkupapi', '0006_golfer_friends_alter_match_message_delete_friendship'),
    ]

    operations = [
        migrations.AddField(
            model_name='golfer',
            name='matches',
            field=models.ManyToManyField(related_name='players', to='linkupapi.match'),
        ),
        migrations.AddField(
            model_name='match',
            name='golfers',
            field=models.ManyToManyField(related_name='my_matches', through='linkupapi.GolferMatch', to='linkupapi.golfer'),
        ),
        migrations.AlterField(
            model_name='golfer',
            name='friends',
            field=models.ManyToManyField(related_name='followers', to='linkupapi.golfer'),
        ),
        migrations.AlterField(
            model_name='golfermatch',
            name='golfer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='linkupapi.golfer'),
        ),
        migrations.AlterField(
            model_name='golfermatch',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='linkupapi.match'),
        ),
    ]
