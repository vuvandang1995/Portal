# Generated by Django 2.1.2 on 2018-11-14 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0013_myuser_token_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='token_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
