# Generated by Django 2.1.5 on 2019-03-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('axf', '0003_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.CharField(max_length=20)),
                ('userid', models.CharField(max_length=20)),
                ('progress', models.IntegerField()),
            ],
            options={
                'db_table': 'order',
            },
        ),
    ]
