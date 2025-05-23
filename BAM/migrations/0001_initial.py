# Generated by Django 5.1.3 on 2024-11-29 16:14

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=30)),
                ('account_no', models.IntegerField(blank=True)),
                ('account_type', models.CharField(choices=[('Checking', 'Checking Account'), ('Savings', 'Savings Account '), ('BO', 'Beneficiary Owners Account'), ('FDR', 'Fixed Deposit Account'), ('RD/DPS', 'Recurring Deposit Account'), ('CDs', 'Certificate of Deposit Account')], max_length=10)),
                ('custodial_name', models.CharField(max_length=20)),
                ('account_balance', models.FloatField(default=0.0)),
                ('opening_date', models.DateField(default=datetime.date.today)),
                ('non_expenditure_account', models.BooleanField()),
                ('last_update_date', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InterAccountTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(default=0.0)),
                ('details', models.TextField(null=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('from_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_account', to='BAM.accounts')),
                ('to_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_account', to='BAM.accounts')),
            ],
        ),
    ]
