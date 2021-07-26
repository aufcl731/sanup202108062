from rest_framework import serializers
from .models import *
from  order.models import *


class Design_Serializer(serializers.ModelSerializer):
    class Meta:
        model = FSTY_CAD_Design_Data
        fields = ('pk', 'CAD_Design_Data_name', 'CAD_Design_Data_xml', 'CAD_Design_Data_pattern_image',
                  'CAD_Design_Data_simulation_image', 'CAD_Design_Data_code', 'CAD_Design_Data_create_date')