# Generated by Django 2.1.1 on 2018-09-17 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0007_server'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='created',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='host',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='ip',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
