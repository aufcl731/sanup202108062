from django.db import models

from order.models import Order_DesignData
from machine.models import Knit_Machine, Warp_Machine, YW_Knit_Machine, YW_Warp_Machine
from materials.models import Beam, Yarn

# Create your models here.
class Knit_Process(models.Model):
    order_designdata = models.OneToOneField(Order_DesignData, on_delete=models.CASCADE)
    knit_machine_id = models.ForeignKey(Knit_Machine, related_name='knit_machine_code', null=True, on_delete=models.CASCADE)
    yw_knit_machine_id = models.ForeignKey(YW_Knit_Machine, null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)
    real_start_time = models.DateTimeField(null=True, default=None)
    real_end_time = models.DateTimeField(null=True, default=None)
    #beam = models.ForeignKey(Beam, null=True)

    class Meta:
        db_table = 'Knit_Process'


class Knit_Beam(models.Model):
    knit_process = models.ForeignKey(Knit_Process, on_delete=models.CASCADE)
    beam = models.ForeignKey(Beam, on_delete=models.CASCADE)
    knit_external = models.IntegerField(null=True)
    knit_current_external = models.IntegerField(null=True)
    knit_turn_cnt = models.IntegerField(null=True)
    knit_current_turn_cnt = models.IntegerField(null=True)
    knit_yarn_thick = models.IntegerField(null=True)
    #knit_yarn = models.ForeignKey(Yarn, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'Knit_Beam'


class Warp_Process(models.Model):
    order_designdata = models.OneToOneField(Order_DesignData, on_delete=models.CASCADE)
    warp_machine_id = models.ForeignKey(Warp_Machine, null=True, on_delete=models.CASCADE)
    yw_warp_machine_id = models.ForeignKey(YW_Warp_Machine, null=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, default=None)
    end_time = models.DateTimeField(null=True, default=None)
    real_start_time = models.DateTimeField(null=True, default=None)
    real_end_time = models.DateTimeField(null=True, default=None)

    #beam = models.ForeignKey(Warp_Beam, null=True)

    class Meta:
        db_table = 'Warp_Process'


class Warp_Beam(models.Model):
    warp_process = models.ForeignKey(Warp_Process, on_delete=models.CASCADE) #스케쥴 FK
    beam = models.ForeignKey(Beam, on_delete=models.CASCADE) #공빔 FK
    external = models.IntegerField(null=True) #실 감겨진 상태의 둘레
    current_external = models.IntegerField(null=True) # 현재 빔 둘레
    turn_cnt = models.IntegerField(null=True) # 생산 후 처음 회전수
    current_turn_cnt = models.IntegerField(null=True) #현재 잔량 회전수
    yarn_thick = models.IntegerField(null=True) #정경된 실두꼐 (외경 - 내경) / 턴수
    yarn_count = models.IntegerField(null=True) #실가락수 (정경본수)
    yarn_meter = models.IntegerField(null=True) #감겨진 실의 길이
    yarn_current_meter = models.IntegerField(null=True) #사용 이후 잔량 실 길이
   #yarn = models.ForeignKey(Yarn, on_delete=models.CASCADE, null=True) #실 FK


    class Meta:
        db_table = 'Warp_Beam'


class Knit_Machine_Realtime(models.Model):
    knit_process = models.ForeignKey(Knit_Process, null=True, on_delete=models.CASCADE)
    trs_operation_number = models.IntegerField(null=True)
    trs_total_run_course = models.IntegerField(null=True)
    trs_state = models.IntegerField(null=True)
    trs_stopmark = models.IntegerField(null=True)
    trs_onetime_prdt = models.IntegerField(null=True)
    trs_set_prdt = models.IntegerField(null=True)
    trs_run_course = models.IntegerField(null=True)
    trs_total_oper_time = models.DateTimeField(null=True)
    trs_total_accum_time = models.DateTimeField(null=True)
    trs_meter = models.FloatField(null=True)
    trs_total_meter = models.IntegerField(null=True)
    trs_accumulate_meter = models.IntegerField(null=True)
    trs_key_angle = models.IntegerField(null=True)
    trs_rpm_main = models.IntegerField(null=True)
    trs_sensor_01 = models.IntegerField(null=True)
    trs_sensor_02 = models.IntegerField(null=True)
    trs_sensor_03 = models.IntegerField(null=True)
    trs_sensor_04 = models.IntegerField(null=True)
    trs_sensor_05 = models.IntegerField(null=True)
    trs_sensor_06 = models.IntegerField(null=True)
    trs_sensor_07 = models.IntegerField(null=True)
    trs_sensor_08 = models.IntegerField(null=True)
    trs_sensor_09 = models.IntegerField(null=True)
    trs_sensor_10 = models.IntegerField(null=True)
    trs_onoff = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Knit_Machine_Realtime'


class Warp_Machine_Realtime(models.Model):
    warp_process = models.ForeignKey(Warp_Process, null=True, on_delete=models.CASCADE)
    tws_start_date = models.DateTimeField(null=True)
    tws_start_time = models.DateTimeField(null=True)
    tws_meter = models.IntegerField(null=True)
    tws_state = models.IntegerField(null=True)
    tws_hoist_state = models.IntegerField(null=True)
    tws_oiling_state = models.IntegerField(null=True)
    tws_clamp_state = models.IntegerField(null=True)
    tws_w_inverter_state = models.IntegerField(null=True)
    tws_s_inverter_state = models.IntegerField(null=True)
    tws_c_inverter_state = models.IntegerField(null=True)
    tws_current_turncnt = models.IntegerField(null=True)
    tws_runtime = models.DateTimeField(null=True)
    tws_current_meter = models.IntegerField(null=True)
    tws_kia = models.IntegerField(null=True)
    tws_warper_speed = models.FloatField(null=True)
    tws_warper_outside = models.IntegerField(null=True)
    tws_warper_total_length = models.FloatField(null=True)
    tws_creel_total_length = models.IntegerField(null=True)
    tws_creel_speed = models.IntegerField(null=True)
    tws_elongation_rate = models.IntegerField(null=True)
    tws_relax_deviation = models.IntegerField(null=True)
    tws_error = models.DateTimeField(null=True)
    tws_onoff = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'Warp_Machine_Realtime'

