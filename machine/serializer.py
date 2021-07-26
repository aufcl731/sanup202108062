from rest_framework import serializers
from .models import *


class Warp_machine_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Warp_Machine
        fields = ('pk', 'tns_code', 'user_id', 'company_code', 'tws_installation_time', 'tws_ip')

class Knit_machine_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Knit_Machine
        fields = ('pk', 'tns_code', 'user_id', 'company_code', 'trs_installation_time', 'trs_model_name', 'trs_beam_cnt',
                  'trs_bar_cnt', 'trs_rpm_main', 'trs_eac_enable', 'trs_tempo', 'trs_lowmotor_enable', 'trs_gauge',
                  'trs_ip')