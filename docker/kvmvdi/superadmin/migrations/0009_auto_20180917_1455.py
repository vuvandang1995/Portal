# Generated by Django 2.1.1 on 2018-09-17 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0008_auto_20180917_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='owner',
        ),
        migrations.DeleteModel(
            name='Server',
        ),
    ]