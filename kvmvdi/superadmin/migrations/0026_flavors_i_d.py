# Generated by Django 2.1.2 on 2018-11-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0025_auto_20181129_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='flavors',
            name='i_d',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
