from django.db import models


def upload_product_file(instance, filename):
    return filename


class FSTY_CAD_Design_Data(models.Model):
    CAD_Design_Data_id = models.AutoField(primary_key=True)
    CAD_Design_Data_name = models.CharField(max_length=100, null=True)
    CAD_Design_Data_code = models.CharField(max_length=100, null=True)
    CAD_Design_Data_xml = models.FileField(upload_to=upload_product_file, null=True)
    CAD_Design_Data_pattern_image = models.ImageField(upload_to=upload_product_file, null=True)
    CAD_Design_Data_simulation_image = models.ImageField(upload_to=upload_product_file, null=True)
    CAD_Design_Data_create_date = models.DateTimeField(auto_now_add=True, blank=True)
    CAD_Design_Data_trc_file = models.FileField(upload_to=upload_product_file, null=True)
    CAD_Design_Data_magnification = models.CharField(max_length=10, null=True, blank=True)
    Linkage_code = models.CharField(max_length=5000, null=True, default=None)

    class Meta:
        db_table = 'FSTY_CAD_Design_Data'

    def __str__(self):
        return self.CAD_Design_Data_name


class FSTY_CAD_Production(models.Model):
    CAD_Production_id = models.AutoField(primary_key=True)
    CAD_Production_quota_per_day = models.CharField(max_length=100, null=True)
    CAD_Production_machine_name = models.CharField(max_length=100, null=True)
    CAD_Production_note = models.CharField(max_length=100, null=True)
    CAD_Production_design_data = models.OneToOneField(FSTY_CAD_Design_Data, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'FSTY_CAD_Production'


class FSTY_CAD_Fabric(models.Model):
    CAD_Fabric_id = models.AutoField(primary_key=True)
    fabric_type = (
        ('R', u'row'),
        ('S', u'simulated')
    )
    CAD_Fabric_type = models.CharField(max_length=1, choices=fabric_type, null=True)
    CAD_Fabric_wpi = models.CharField(max_length=100, null=True)
    CAD_Fabric_cpi = models.CharField(max_length=100, null=True)
    CAD_Fabric_width = models.CharField(max_length=100, null=True)
    CAD_Fabric_weight_per_width = models.CharField(max_length=100, null=True)
    CAD_Fabric_production = models.ForeignKey(FSTY_CAD_Production, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'FSTY_CAD_Fabric'


class FSTY_CAD_Layer(models.Model):
    CAD_Layer_id = models.AutoField(primary_key=True)
    CAD_Layer_name = models.CharField(max_length=100, null=True)
    CAD_Layer_ratio = models.CharField(max_length=100, null=True)
    CAD_Layer_mm_rack = models.CharField(max_length=100, null=True)
    CAD_Layer_use = models.CharField(max_length=100, null=True)
    CAD_Layer_beam = models.CharField(max_length=100, null=True)
    CAD_Layer_total = models.CharField(max_length=100, null=True)
    CAD_Layer_iodata = models.CharField(max_length=2000, null=True)
    CAD_Layer_design_data = models.ForeignKey(FSTY_CAD_Design_Data, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'FSTY_CAD_Layer'


class FSTY_CAD_Yarn(models.Model):
    CAD_Yarn_id = models.AutoField(primary_key=True)
    CAD_Yarn_idx = models.CharField(max_length=100, null=True)
    CAD_Yarn_maker = models.CharField(max_length=100, null=True)
    CAD_Yarn_spec = models.CharField(max_length=100, null=True)
    CAD_Yarn_code = models.CharField(max_length=100, null=True)
    CAD_Yarn_rgb_color = models.CharField(max_length=100, null=True)
    CAD_Yarn_lab_color = models.CharField(max_length=100, null=True)
    CAD_Yarn_pantone_color = models.CharField(max_length=100, null=True)
    CAD_Yarn_layer = models.OneToOneField(FSTY_CAD_Layer, on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = 'FSTY_CAD_Yarn'


class FSTY_CAD_Chain_Link(models.Model):
    CAD_Chain_Link_id = models.AutoField(primary_key=True)
    CAD_Chain_Link_course = models.CharField(max_length=2000)
    CAD_Chain_Link_layer = models.OneToOneField(FSTY_CAD_Layer, on_delete=models.CASCADE, null=True)


    class Meta:
        db_table = 'FSTY_CAD_Chain_Link'
