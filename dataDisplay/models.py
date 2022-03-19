from django.db import models
from django.contrib.auth.models import User


class Map(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    map_data = models.JSONField()


class PeriodOfTheYear(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False)


class CategoryOfWorks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(blank=False)


class IndicationLimits(models.Model):
    id = models.AutoField(primary_key=True)
    UpperHumidityLimit = models.IntegerField()
    UpperTemperatureLimit = models.IntegerField()
    LowerHumidityLimit = models.IntegerField()
    LowerTemperatureLimit = models.IntegerField()


class Manual(models.Model):
    id = models.AutoField(primary_key=True)
    PeriodOfTheYear_id = models.ForeignKey(PeriodOfTheYear, on_delete=models.CASCADE)
    CategoryOfWorks_id = models.ForeignKey(CategoryOfWorks, on_delete=models.CASCADE)
    IndicationLimits_id = models.ForeignKey(IndicationLimits, on_delete=models.CASCADE)


class UserManual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Manual_id = models.OneToOneField(Manual, on_delete=models.CASCADE)


class Sensor(models.Model):
    id = models.AutoField(primary_key=True)
    Api_key = models.TextField(blank=False)
    Name = models.TextField(blank=False)
    Description = models.TextField(blank=False)
    User = models.ForeignKey(User, on_delete=models.CASCADE)


class Indications(models.Model):
    id = models.AutoField(primary_key=True)
    Receiving_data_time = models.IntegerField(blank=False)
    Humidity = models.FloatField(blank=False)
    Temperature = models.FloatField(blank=False)
    Sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)


class DeviationsIndications(models.Model):
    id = models.AutoField(primary_key=True)
    Indications_id = models.ForeignKey(Indications, on_delete=models.CASCADE)
