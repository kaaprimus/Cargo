# Generated by Django 4.2.3 on 2023-07-06 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_room_alter_customuser_user_type_message"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="company",
            new_name="carrier_company",
        ),
        migrations.AddField(
            model_name="order",
            name="shipper_company",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="main.shippercompany",
            ),
        ),
    ]
