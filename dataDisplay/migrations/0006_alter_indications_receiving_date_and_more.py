# Generated by Django 4.0.3 on 2022-03-03 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataDisplay', '0005_indications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indications',
            name='Receiving_date',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='indications',
            name='Receiving_time',
            field=models.TextField(),
        ),
    ]
