# Generated by Django 3.0.4 on 2020-03-25 12:19

import cms.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copyshop', '0003_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='assignee',
            field=cms.fields.CharField(blank=True, verbose_name='in behandeling door'),
        ),
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='totaalbedrag'),
            preserve_default=False,
        ),
    ]