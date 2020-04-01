from django.db import models
from design_data.models import *
from datetime import datetime
# Create your models here.
class Yarn(models.Model):

    name = models.CharField(max_length=25, null=True)
    code = models.CharField(max_length=25, null=True)
    type = models.CharField(max_length=25, null=True)
    maker = models.CharField(max_length=25, null=True) #메이커
    count = models.IntegerField(null=True) #굵기
    filament = models.IntegerField(null=True) #필라멘트
    contraction = models.IntegerField(null=True) #수축률
    material = models.CharField(max_length=10, null=True) #재료
    kind = models.CharField(max_length=25, null=True) #종류
    color = models.CharField(max_length=25, null=True) #색
    weght = models.IntegerField(default=0)#무게
    qty = models.IntegerField(default=0) #수
    Receivingdate = models.CharField(default=datetime.now().strftime('%Y-%m-%d %H:%M'), max_length=30)#입고날짜

    class Meta:
        db_table = 'Fabric_Yarn'


class Beam(models.Model):
    name = models.CharField(max_length=25, null=True)
    yarn = models.ForeignKey(Yarn, on_delete=models.CASCADE, null=True)
    yarn_qty = models.IntegerField(default=0)
    size = models.IntegerField(null=True)
    Receivingdate = models.CharField(default=datetime.now().strftime('%Y-%m-%d %H:%M'), max_length=30)

    class Meta:
        db_table = 'Fabric_Beam'


class Raw(models.Model):
    designData_id = models.ForeignKey(FSTY_CAD_Design_Data, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)

    class Meta:
        db_table = 'Fabric_Raw'

class Roll(models.Model):
    rollname = models.CharField(max_length=25, null=True)
    rollfabricname = models.CharField(max_length=30, null=True)
    rollfabricdate = models.DateField(null=True, default=None)
    rolloutdate = models.DateField(null=True, default=None)
    receivingdate =models.DateField(default=datetime.now())
    rollcount = models.IntegerField(null=False)
    rollfabricerror = models.IntegerField(null=False)
    rollfabrictrue = models.IntegerField(null=False)
    rollfabriclength = models.IntegerField(null=False)
    rollfabricweight = models.IntegerField(null=False)
    class Meta:
        db_table = 'Fabric_Roll'


class RawRoll(models.Model):
    raw_id = models.ForeignKey(Raw, on_delete=models.CASCADE)
    raw_yard = models.IntegerField(default=0)
    raw_weight = models.IntegerField(default=0)

    class Meta:
        db_table = 'Fabric_RawRoll'