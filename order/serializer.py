from rest_framework import serializers
from .models import *


class Order_design_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order_DesignData
        fields = ('pk', 'order_id', 'code', 'design_data_id', 'design_qty', 'qr_code')

class Order_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('pk', 'company', 'code', 'buyer', 'type', 'state', 'order_date', 'due_date', 'order_round',
                  'order_inout', 'cheack', 'manager_id')