# Generated by Django 3.0.2 on 2020-04-07 17:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racetime', '0024_user_favourite_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='custom_profile_slug',
            field=models.SlugField(blank=True, help_text='If set, this will allow you to have a custom URL for your user profile, like https://racetime.gg/user/supermario64. You may only use letters, numbers, hyphens and underscores. This is a staff/supporter feature. If you lose your status, your profile will revert back to its regular URL.', max_length=25, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Custom profile URL'),
        ),
    ]
