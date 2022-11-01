# Generated by Django 3.2.15 on 2022-10-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0001_init'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='reference_id',
            field=models.CharField(blank=True, db_index=True, help_text='The identifier of the item acquired via the transaction.e.g. a course enrollment ID, an entitlement ID, a subscription license ID.', max_length=255, null=True),
        ),
    ]
