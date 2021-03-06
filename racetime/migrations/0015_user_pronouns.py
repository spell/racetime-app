# Generated by Django 3.0.2 on 2020-03-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racetime', '0014_userranking_best_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pronouns',
            field=models.CharField(blank=True, choices=[('', 'None'), ('she/her', 'Feminine (she/her)'), ('he/him', 'Masculine (he/him)'), ('they/them', 'Neutral (they/them)')], help_text='Select which pronouns appear next to your name on the site.', max_length=16, null=True, verbose_name='Preferred pronouns'),
        ),
    ]
