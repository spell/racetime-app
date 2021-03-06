# Generated by Django 3.0.1 on 2020-01-18 10:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('racetime', '0006_auto_20200117_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrant',
            name='score_change',
            field=models.FloatField(null=True),
        ),
        migrations.CreateModel(
            name='UserRanking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(db_index=True, default=0.0)),
                ('confidence', models.FloatField(default=0.0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='racetime.Category')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='racetime.Goal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
