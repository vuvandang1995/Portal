# Generated by Django 2.1.2 on 2018-11-29 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0024_auto_20181129_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flavors',
            name='ram',
            field=models.IntegerField(),
        ),
    ]
