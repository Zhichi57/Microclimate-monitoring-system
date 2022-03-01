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
    PeriodOfTheYear_id = models.OneToOneField(PeriodOfTheYear, on_delete=models.CASCADE)
    CategoryOfWorks_id = models.OneToOneField(CategoryOfWorks, on_delete=models.CASCADE)
    IndicationLimits_id = models.OneToOneField(IndicationLimits, on_delete=models.CASCADE)


class UserManual(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Manual_id = models.OneToOneField(Manual, on_delete=models.CASCADE)

