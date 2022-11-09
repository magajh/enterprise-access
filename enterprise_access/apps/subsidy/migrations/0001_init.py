# Generated by Django 3.2.15 on 2022-11-09 16:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LearnerCreditAccessPolicy',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('group_uuid', models.UUIDField(blank=True, db_index=True, null=True)),
                ('catalog_uuid', models.UUIDField(blank=True, db_index=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubscriptionAccessPolicy',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('group_uuid', models.UUIDField(blank=True, db_index=True, null=True)),
                ('catalog_uuid', models.UUIDField(blank=True, db_index=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LicenseRequestAccessPolicy',
            fields=[
                ('subscriptionaccesspolicy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subsidy.subscriptionaccesspolicy')),
            ],
            options={
                'abstract': False,
            },
            bases=('subsidy.subscriptionaccesspolicy',),
        ),
        migrations.CreateModel(
            name='PerLearnerEnrollmentCapLearnerCreditAccessPolicy',
            fields=[
                ('learnercreditaccesspolicy_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='subsidy.learnercreditaccesspolicy')),
                ('per_learner_cap', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=('subsidy.learnercreditaccesspolicy',),
        ),
        migrations.CreateModel(
            name='SubscriptionSubsidy',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('starting_balance', models.BigIntegerField()),
                ('unit', models.CharField(choices=[('usd_cents', 'U.S. Dollar (Cents)'), ('seats', 'Seats in a course'), ('jpy', 'Japanese Yen')], db_index=True, default='usd_cents', max_length=255)),
                ('opportunity_id', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_uuid', models.CharField(max_length=255)),
                ('active_datetime', models.DateTimeField(default=None, null=True)),
                ('expiration_datetime', models.DateTimeField(default=None, null=True)),
                ('subscription_plan_uuid', models.UUIDField(db_index=True)),
                ('ledger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ledger.ledger')),
            ],
        ),
        migrations.AddField(
            model_name='subscriptionaccesspolicy',
            name='subsidy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subsidy.subscriptionsubsidy'),
        ),
        migrations.CreateModel(
            name='LearnerCreditSubsidy',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('starting_balance', models.BigIntegerField()),
                ('unit', models.CharField(choices=[('usd_cents', 'U.S. Dollar (Cents)'), ('seats', 'Seats in a course'), ('jpy', 'Japanese Yen')], db_index=True, default='usd_cents', max_length=255)),
                ('opportunity_id', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_uuid', models.CharField(max_length=255)),
                ('active_datetime', models.DateTimeField(default=None, null=True)),
                ('expiration_datetime', models.DateTimeField(default=None, null=True)),
                ('ledger', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ledger.ledger')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='learnercreditaccesspolicy',
            name='subsidy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subsidy.learnercreditsubsidy'),
        ),
    ]
