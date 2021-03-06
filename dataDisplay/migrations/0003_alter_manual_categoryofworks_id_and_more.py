# Generated by Django 4.0.3 on 2022-03-02 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataDisplay', '0002_categoryofworks_indicationlimits_manual_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manual',
            name='CategoryOfWorks_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataDisplay.categoryofworks'),
        ),
        migrations.AlterField(
            model_name='manual',
            name='IndicationLimits_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataDisplay.indicationlimits'),
        ),
        migrations.AlterField(
            model_name='manual',
            name='PeriodOfTheYear_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataDisplay.periodoftheyear'),
        ),
    ]
