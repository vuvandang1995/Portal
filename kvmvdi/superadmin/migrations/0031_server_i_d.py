# Generated by Django 2.1.3 on 2018-12-12 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0030_auto_20181210_1349'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='i_d',
            field=models.CharField(max_length=255, null=True),
        ),
    ]