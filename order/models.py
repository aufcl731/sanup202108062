from django.db import models
from django.utils import timezone

from account.models import User
from design_data.models import FSTY_CAD_Design_Data

# Create your models here.
class Order(models.Model):
    company = models.CharField(max_length=100, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE) # User 참조해야하는지 확인해봐야겠음.
    code = models.CharField(max_length=100, null=True) # order_date + round
    buyer = models.CharField(max_length=100, null=True)
    type = models.IntegerField(null=True) #0 샘플 , 1 메인
    state = models.IntegerField(null=True, default=0) #0 대기, 1.진행, 2.완료
    order_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    order_round = models.IntegerField(default=1, null=True)
    order_inout = models.IntegerField(default=0, null=True)
    cheack = models.BooleanField(default=False)
    value = models.BooleanField(default=False)
    knitWorkKey = models.CharField(max_length=100) # knitWorkKey

    class Meta:
        db_table = 'Fabric_Order'


class Order_DesignData(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_design')
    code = models.CharField(max_length=100, null=True) # order_code - i
    design_data_id = models.ForeignKey(FSTY_CAD_Design_Data, on_delete=models.CASCADE)
    design_qty = models.IntegerField(null=True)
    #weight = models.IntegerField(default=0)
    #weight_per_yard = models.IntegerField(null=True, default=0)
    qr_code = models.ImageField(upload_to='', null=True)
    # knitWorkKey = models.Field(Order, on_delete=models.CASCADE)
    # knitWorkKey = models.CharField(max_length=100, null=True)  # knitWorkKey

    class Meta:
        db_table = 'Fabric_Order_DesignData'


'''주문자 연계 추가'''
class Style_yarn(models.Model):
    st_yarn_code = models.CharField(max_length=200)
    st_yarn_name = models.CharField(max_length=200)
    st_yarn_color = models.CharField(max_length=100)
    st_yarn_rate = models.FloatField()
    st_yarn_cnt = models.FloatField()
    yn_Dye = models.BooleanField()

class Style_fabric(models.Model):
    fabric_code = models.CharField(max_length=500, primary_key=True)
    fabric_name = models.CharField(max_length=500)
    fabric_color = models.CharField(max_length=150)
    fabric_size = models.CharField(max_length=200)
    fabric_part = models.CharField(max_length=250)
    fabric_Construction = models.CharField(max_length=600)
    FabricLoss = models.FloatField(null=True)
    FabricCsm = models.FloatField(null=True)
    fabric_width = models.FloatField()
    cuttable_width = models.FloatField()
    sMeter_width = models.FloatField()
    yard_weight = models.FloatField()
    unit = models.CharField(max_length=200)
    fabric_Csm = models.FloatField()
    fabric_Mrp = models.FloatField()
    dyeProcessTypeCode = models.CharField(max_length=100)
    dyeCompanyCode = models.CharField(max_length=1000, null=True)
    knitCompanyCode = models.CharField(max_length=1000, null=True)
    dyeProcessTypeName = models.CharField(max_length=100)
    dyeCompanyName = models.CharField(max_length=100)
    knitCompanyName = models.CharField(max_length=100)
    yarn = models.ForeignKey(Style_yarn, on_delete=models.CASCADE, null=True)

class Style_orders(models.Model):
    style_key = models.CharField(max_length=500)
    factory_code = models.CharField(max_length=100)
    factory_name = models.CharField(max_length=100, null=True)
    style_ver = models.CharField(max_length=100)
    fabric_info = models.ForeignKey(Style_fabric, on_delete=models.CASCADE)
    design_ck = models.BooleanField(default=False)