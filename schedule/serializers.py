from rest_framework import serializers
from .models import *
from machine.models import *


class Knit_machine_code(serializers.ModelSerializer):

    class Meta:
        model = Knit_Machine
        fields = '__all__'

class design_data_code(serializers.ModelSerializer):

    class Meta:
        model = Order_DesignData
        fields = '__all__'

class Knit_process_Serializer(serializers.ModelSerializer):

    knit_machine_code = Knit_machine_code(many=True, read_only=True)
    design_data_code = design_data_code(many=True, read_only=True)

    class Meta:
        model = Knit_Process
        fields = ('pk', 'start_time', 'end_time', 'real_start_time', 'real_end_time', 'knit_machine_id',
                  'order_designdata_id', 'yw_knit_machine_id_id', 'knit_machine_code', 'design_data_code')


class Warp_process_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Warp_Process
        fields = ('pk', 'start_time', 'end_time', 'real_start_time', 'real_end_time', 'order_designdata_id',
                  'warp_machine_id_id', 'yw_warp_machine_id_id')
