# Generated by Django 3.0.4 on 2020-04-01 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copyshop', '0007_auto_20200325_2122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_url',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('open', 'nog niet betaald'), ('canceled', 'betaling geannuleerd'), ('expired', 'betaling verlopen'), ('failed', 'betaling mislukt'), ('paid', 'betaald')], default='open', max_length=32, verbose_name='status'),
        ),
    ]