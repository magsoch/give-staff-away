# Generated by Django 2.2.1 on 2019-06-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20190604_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donate',
            name='form_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
