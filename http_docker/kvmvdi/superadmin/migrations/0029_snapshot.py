# Generated by Django 2.1.3 on 2018-12-10 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0028_auto_20181206_1423'),
    ]

    operations = [
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.CharField(max_length=255, null=True)),
                ('ops', models.ForeignKey(db_column='ops', on_delete=django.db.models.deletion.CASCADE, to='superadmin.Ops')),
                ('owner', models.ForeignKey(db_column='owner', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'snapshot',
                'managed': True,
            },
        ),
    ]
