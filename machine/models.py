from django.db import models

# Create your models here.
from account.models import Company


class Warp_Machine(models.Model):
    tns_code = models.CharField(max_length=50, null=True)
    user_id = models.CharField(max_length=50, null=True) #작업자는 항상 변경됨
    company_code = models.CharField(max_length=50, null=True) #User에 존재함
    tws_name = models.CharField(max_length=50, null=True)
    tws_installation_time = models.DateTimeField(null=True) #등록시간으로 사용하겠음. Ver.영우
    tws_ip = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'Warp_Machine'


class Knit_Machine(models.Model):
    tns_code = models.CharField(max_length=50, null=True)
    user_id = models.CharField(max_length=50, null=True)
    company_code = models.CharField(max_length=50, null=True)
    trs_installation_time = models.DateTimeField(null=True)
    trs_model_name = models.CharField(max_length=50, null=True)
    trs_beam_cnt = models.IntegerField(null=True)
    trs_bar_cnt = models.IntegerField(null=True)
    trs_rpm_main = models.IntegerField(null=True)
    trs_eac_enable = models.IntegerField(null=True)
    trs_tempo = models.IntegerField(null=True)
    trs_lowmotor_enable = models.IntegerField(null=True)
    trs_gauge = models.IntegerField(null=True)
    trs_ip = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'Knit_Machine'



class YW_Knit_Machine(models.Model):
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    create_data = models.DateTimeField(auto_now_add=True)
    rpm = models.IntegerField(null=True)
    gauge = models.IntegerField(null=True)
    bar_cnt = models.IntegerField(null=True)

    class Meta:
        db_table = 'yw_knit_machine'


class YW_Warp_Machine(models.Model):
    name = models.CharField(max_length=50, null=True)
    code = models.CharField(max_length=50, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'yw_warp_machine'