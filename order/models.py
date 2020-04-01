from django.db import models
from django.utils import timezone

from account.models import User
from design_data.models import FSTY_CAD_Design_Data

# Create your models here.
class Order(models.Model):
    company = models.CharField(max_length=25, null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE) # User 참조해야하는지 확인해봐야겠음.
    code = models.CharField(max_length=25, null=True) # order_date + round
    buyer = models.CharField(max_length=10, null=True)
    type = models.IntegerField(null=True) #0 샘플 , 1 메인
    state = models.IntegerField(null=True, default=0) #0 대기, 1.진행, 2.완료
    order_date = models.DateTimeField(null=True)
    due_date = models.DateTimeField(null=True)
    order_round = models.IntegerField(default=1, null=True)
    order_inout = models.IntegerField(default=0, null=True)
    cheack = models.BooleanField(default=False)

    class Meta:
        db_table = 'Fabric_Order'


class Order_DesignData(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    code = models.CharField(max_length=25, null=True) # order_code - i
    design_data_id = models.ForeignKey(FSTY_CAD_Design_Data, on_delete=models.CASCADE)
    design_qty = models.IntegerField(null=True)
    #weight = models.IntegerField(default=0)
    #weight_per_yard = models.IntegerField(null=True, default=0)
    qr_code = models.ImageField(upload_to='', null=True)

    class Meta:
        db_table = 'Fabric_Order_DesignData'