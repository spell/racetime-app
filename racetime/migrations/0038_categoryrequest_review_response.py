# Generated by Django 3.0.7 on 2020-06-28 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racetime', '0037_auto_20200620_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoryrequest',
            name='review_response',
            field=models.TextField(blank=True, help_text='Visible to the user. If you wish to tell the user something about their request (especially when rejecting), use this field. Make sure to write this BEFORE accepting/rejecting the category.'),
        ),
    ]
