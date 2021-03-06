# Generated by Django 2.1.2 on 2018-11-23 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0019_flavors'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('ops', models.ForeignKey(db_column='ops', on_delete=django.db.models.deletion.CASCADE, to='superadmin.Ops')),
            ],
            options={
                'db_table': 'images',
                'managed': True,
            },
        ),
    ]
