# Generated by Django 3.0.4 on 2020-03-25 17:36

import cms.fields
import copyshop.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copyshop', '0005_order_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='token',
            field=cms.fields.CharField(blank=True, default=copyshop.models.get_token),
        ),
    ]
