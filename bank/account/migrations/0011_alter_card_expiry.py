# Generated by Django 4.2.7 on 2023-11-27 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0010_card_cvv_alter_card_alias_alter_card_expiry_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card",
            name="expiry",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2028, 11, 25, 17, 53, 53, 318087, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
