# Generated by Django 2.2.18 on 2021-02-06 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20210205_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=255),
        ),
    ]
