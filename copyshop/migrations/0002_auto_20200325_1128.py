# Generated by Django 3.0.4 on 2020-03-25 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copyshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hour',
            name='day',
            field=models.CharField(choices=[('Ma', 'Maandag'), ('Di', 'Dinsdag'), ('Wo', 'Woensdag'), ('Do', 'Donderdag'), ('Vr', 'Vrijdag'), ('Za', 'Zaterdag'), ('Zo', 'Zondag')], max_length=2, verbose_name='Dag'),
        ),
    ]
