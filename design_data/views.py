import json

from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xml.etree.ElementTree import parse

from django.views.generic import DetailView

import config.settings as settings
from design_data.models import *

from django.shortcuts import render, redirect
from order.models import *
from design_data.style_for_us_image_upload import style_for_us_image_upload


@csrf_exempt
def designDataByJson(request):
    jsonDesignObj = {}
    designId = request.POST.get('designId', None)
    designObj = FSTY_CAD_Design_Data.objects.get(CAD_Design_Data_id=designId)
    layerList = FSTY_CAD_Layer.objects.filter(CAD_Layer_design_data=designObj)
    fabricList = FSTY_CAD_Fabric.objects.filter(CAD_Fabric_production=designObj.fsty_cad_production)

    jsonFabricList = []
    for fabricObj in fabricList:
        jsonFabricObj = {}
        jsonFabricObj['CAD_Fabric_id'] = fabricObj.CAD_Fabric_id
        jsonFabricObj['CAD_Fabric_type'] = fabricObj.CAD_Fabric_type
        jsonFabricObj['CAD_Fabric_wpi'] = fabricObj.CAD_Fabric_wpi
        jsonFabricObj['CAD_Fabric_cpi'] = fabricObj.CAD_Fabric_cpi
        jsonFabricObj['CAD_Fabric_width'] = fabricObj.CAD_Fabric_width
        jsonFabricObj['CAD_Fabric_weight_per_width'] = fabricObj.CAD_Fabric_weight_per_width
        jsonFabricList.append(jsonFabricObj)

    jsonLayerList = []
    for layerObj in layerList:
        jsonLayerObj = {}
        jsonLayerObj['CAD_Layer_id'] = layerObj.CAD_Layer_id
        jsonLayerObj['CAD_Layer_name'] = layerObj.CAD_Layer_name
        jsonLayerObj['CAD_Layer_ratio'] = layerObj.CAD_Layer_ratio
        jsonLayerObj['CAD_Layer_mm_rack'] = layerObj.CAD_Layer_mm_rack
        jsonLayerObj['CAD_Layer_use'] = layerObj.CAD_Layer_use
        jsonLayerObj['CAD_Layer_beam'] = layerObj.CAD_Layer_beam
        jsonLayerObj['CAD_Layer_total'] = layerObj.CAD_Layer_total
        jsonLayerObj['CAD_Layer_iodata'] = layerObj.CAD_Layer_iodata
        jsonLayerObj['FSTY_CAD_Yarn'] = {}
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_id'] = layerObj.fsty_cad_yarn.CAD_Yarn_id
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_idx'] = layerObj.fsty_cad_yarn.CAD_Yarn_idx
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_maker'] = layerObj.fsty_cad_yarn.CAD_Yarn_maker
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_spec'] = layerObj.fsty_cad_yarn.CAD_Yarn_spec
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_code'] = layerObj.fsty_cad_yarn.CAD_Yarn_code
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_rgb_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_rgb_color
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_lab_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_lab_color
        jsonLayerObj['FSTY_CAD_Yarn']['CAD_Yarn_pantone_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_pantone_color
        jsonLayerObj['FSTY_CAD_Chain_Link'] = {}
        jsonLayerObj['FSTY_CAD_Chain_Link']['CAD_Chain_Link_id'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_id
        jsonLayerObj['FSTY_CAD_Chain_Link']['CAD_Chain_Link_course'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_course
        jsonLayerList.append(jsonLayerObj)


    jsonDesignObj['CAD_Design_Data_id'] = designObj.CAD_Design_Data_id
    jsonDesignObj['CAD_Design_Data_name'] = designObj.CAD_Design_Data_name
    jsonDesignObj['CAD_Design_Data_code'] = designObj.CAD_Design_Data_code
    jsonDesignObj['CAD_Design_Data_pattern_image'] = designObj.CAD_Design_Data_pattern_image.url
    jsonDesignObj['CAD_Design_Data_simulation_image']= designObj.CAD_Design_Data_simulation_image.url
    jsonDesignObj['CAD_Design_Data_create_date'] = designObj.CAD_Design_Data_create_date.strftime("%Y-%m-%d")
    jsonDesignObj['CAD_Design_Data_magnification'] = designObj.CAD_Design_Data_magnification
    jsonDesignObj['FSTY_CAD_Production'] = {}
    jsonDesignObj['FSTY_CAD_Production']['CAD_Production_id'] = designObj.fsty_cad_production.CAD_Production_id
    jsonDesignObj['FSTY_CAD_Production']['CAD_Production_quota_per_day'] = designObj.fsty_cad_production.CAD_Production_quota_per_day
    jsonDesignObj['FSTY_CAD_Production']['CAD_Production_machine_name'] = designObj.fsty_cad_production.CAD_Production_machine_name
    jsonDesignObj['FSTY_CAD_Production']['CAD_Production_note'] = designObj.fsty_cad_production.CAD_Production_note
    jsonDesignObj['FSTY_CAD_Production']['FSTY_CAD_Fabric'] = jsonFabricList
    jsonDesignObj['FSTY_CAD_Layer'] = jsonLayerList

    return HttpResponse(json.dumps(jsonDesignObj), content_type='application/json')

@login_required(login_url='/')
@csrf_exempt
def delete(request):

    designId = request.POST.get("designId", None)

    if designId != None:
        designObj = FSTY_CAD_Design_Data.objects.get(CAD_Design_Data_id=designId)
        designObj.delete()

    return HttpResponse(json.dumps('{success: true}'), content_type='application/json')

@csrf_exempt
@login_required(login_url='/')
def showList(request):

    designList = FSTY_CAD_Design_Data.objects.all().order_by("-CAD_Design_Data_id")
    orderList = Order.objects.all()

    return render(request, 'designList.html', {'designList': designList, 'count': designList.count(), 'title': 'Design','orderList':orderList})

@csrf_exempt
@login_required(login_url='/')
def showDesign(request, designId):

    print(designId)

    designObj = FSTY_CAD_Design_Data.objects.get(CAD_Design_Data_id=designId)

    return render(request, 'designDetail.html', {'object': designObj, 'title': 'Design'})

@csrf_exempt
@login_required(login_url='/')
def showDesignProduction(request, designId):

    designObj = FSTY_CAD_Design_Data.objects.get(CAD_Design_Data_id=designId)

    return render(request, 'worksheet/knit.html', {'object': designObj})


@csrf_exempt
def designListByJson(request):
    searchName = request.POST['searchName']

    designList = FSTY_CAD_Design_Data.objects.filter(CAD_Design_Data_name__contains=searchName).order_by('-CAD_Design_Data_id')
    jsonList = []
    for obj in designList:
        jsonObj = {}
        jsonObj['id'] = obj.CAD_Design_Data_id
        jsonObj['name'] = obj.CAD_Design_Data_name
        jsonObj['date'] = obj.CAD_Design_Data_create_date.strftime("%Y-%m-%d")
        jsonList.append(jsonObj)

    return HttpResponse(json.dumps(jsonList), content_type='application/json')

# Create your views here.
@csrf_exempt
def upload(request):
    if 'project' in request.FILES:
        print('xml file exist')

        # file catch
        xml_file = request.FILES['project']
        pattern_image = request.FILES['design']
        simulation_image = request.FILES['simulation']

        # project save
        cad_design_data = FSTY_CAD_Design_Data()
        cad_design_data.save()

        xml_file_name = 'data/project/' + str(cad_design_data.CAD_Design_Data_id) + '/xml/' + xml_file.name
        cad_design_data.CAD_Design_Data_xml.save(xml_file_name, ContentFile(xml_file.read()))

        pattern_image_path = 'data/project/' + str(cad_design_data.CAD_Design_Data_id) + '/img/' + pattern_image.name
        cad_design_data.CAD_Design_Data_pattern_image.save(pattern_image_path, ContentFile(pattern_image.read()))

        simulation_image_path = 'data/project/' + str(cad_design_data.CAD_Design_Data_id) + '/img/' + simulation_image.name
        cad_design_data.CAD_Design_Data_simulation_image.save(simulation_image_path, ContentFile(simulation_image.read()))

        reselt = style_for_us_image_upload(request.build_absolute_uri(cad_design_data.CAD_Design_Data_simulation_image.url), simulation_image.name)

        # qr_code_image = qrcode.make('http://211.238.177.143:8888/design_data/'+str(cad_design_data.id)+'/')
        # qr_code_image_path = 'data/project/' + str(cad_design_data.id) + '/img/qr_code_image.png'
        # cad_design_data.qr_code.save(qr_code_image_path, ContentFile(qr_code_image.read()))
        # qr_code_image.save(settings.MEDIA_ROOT + '/data/project/' + str(cad_design_data.id) + '/img/qr_code_image.png')

        project_path = settings.MEDIA_ROOT + '/data/project/' + str(cad_design_data.CAD_Design_Data_id)

        # django 내장 파일업로드 기능이 아닌 부분
        # UPLOAD_DIR = settings.MEDIA_ROOT + 'data/project/' + str(project.id) + '/trc'
        # if not os.path.exists(UPLOAD_DIR):
        #     os.makedirs(UPLOAD_DIR)
        # trc = request.FILES['trc']
        # fp = open('%s/%s' % (UPLOAD_DIR, trc._name), 'wb')
        # for chunk in trc.chunks():
        #     fp.write(chunk)
        # fp.close()

        # django 파일필드 사용 저장
        #trc = request.FILES['trc']
        #trc_name = 'data/project/' + str(cad_design_data.id) + '/trc/' + trc.name
        #cad_design_data.trc_file.save(trc_name, ContentFile(trc.read()))

        print(settings.MEDIA_ROOT + '/' + cad_design_data.CAD_Design_Data_xml.__str__())
        with open(settings.MEDIA_ROOT + '/' + cad_design_data.CAD_Design_Data_xml.__str__(), encoding='UTF-8') as xml:
            doc = parse(xml)
        root = doc.getroot()
        cad_design_data.CAD_Design_Data_name = root.get("name")
        print('cad_name'+cad_design_data.CAD_Design_Data_name)
        cad_design_data.CAD_Design_Data_code = root.get("code")
        cad_design_data.CAD_Design_Data_magnification = root.find("production").find("magnification_ratio").get("value")
        print('cad_code' + cad_design_data.CAD_Design_Data_code)
        cad_design_data.save()

        # Git 테스트 161205
        # production save
        xml_production = root.find("production")
        cad_production = FSTY_CAD_Production()
        print(cad_production)
        cad_production.CAD_Production_quota_per_day = xml_production.find("quota_per_day").get("value")
        cad_production.CAD_Production_machine_name = xml_production.find("machine_name").get("value")
        cad_production.CAD_Production_note = xml_production.find("note").get("value")
        cad_production.CAD_Production_design_data = cad_design_data
        print('aaa')
        cad_production.save()

        # production row save
        xml_row = xml_production.find("row")
        row = FSTY_CAD_Fabric()
        row.CAD_Fabric_type = 'R'
        row.CAD_Fabric_wpi = xml_row.find("wpi").get("value")
        row.CAD_Fabric_cpi = xml_row.find("cpi").get("value")
        row.CAD_Fabric_width = xml_row.find("width").get("value")
        row.CAD_Fabric_weight_per_width = xml_row.find("weight_per_width").get("value")
        row.CAD_Fabric_production = cad_production
        row.save()

        # production simulated save
        xml_simulated = xml_production.find("simulated")
        simulated = FSTY_CAD_Fabric()
        simulated.CAD_Fabric_type = 'S'
        simulated.CAD_Fabric_wpi = xml_simulated.find("wpi").get("value")
        simulated.CAD_Fabric_cpi = xml_simulated.find("cpi").get("value")
        simulated.CAD_Fabric_width = xml_simulated.find("width").get("value")
        simulated.CAD_Fabric_weight_per_width = xml_simulated.find("weight_per_width").get("value")
        simulated.CAD_Fabric_production = cad_production
        simulated.save()

        # Layer save
        for xmlLayer in root.iter("layer"):
            cad_layer = FSTY_CAD_Layer()
            cad_layer.CAD_Layer_name = xmlLayer.get("name")
            cad_layer.CAD_Layer_ratio = xmlLayer.find("ratio").get("value")
            cad_layer.CAD_Layer_mm_rack = xmlLayer.find("mmrack").get("value")
            cad_layer.CAD_Layer_use = xmlLayer.find("use").get("value")
            cad_layer.CAD_Layer_beam = xmlLayer.find("beam").get("value")
            cad_layer.CAD_Layer_total = xmlLayer.find("total").get("value")
            cad_layer.CAD_Layer_design_data = cad_design_data
            xml_inout = xmlLayer.find("inout")
            cad_layer.CAD_Layer_iodata = xml_inout.get("value")
            cad_layer.save()

            # Layer Yarn save
            xml_yarn = xmlLayer.find("yarn")
            cad_yarn = FSTY_CAD_Yarn()
            cad_yarn.CAD_Yarn_idx = xml_yarn.find("idx").get("value")
            cad_yarn.CAD_Yarn_maker = xml_yarn.find("maker").get("value")
            cad_yarn.CAD_Yarn_spec = xml_yarn.find("spec").get("value")
            cad_yarn.CAD_Yarn_code = xml_yarn.find("code").get("value")
            cad_yarn.CAD_Yarn_rgb_color = xml_yarn.find("rgb_color").get("value")
            cad_yarn.CAD_Yarn_lab_color = xml_yarn.find("lab_color").get("value")
            cad_yarn.CAD_Yarn_pantone_color = xml_yarn.find("pantone_color").get("value")
            cad_yarn.CAD_Yarn_layer = cad_layer
            cad_yarn.save()

            # Layer ChainLink save
            xml_chain_link = xmlLayer.find("chainlink")
            cad_chain_link = FSTY_CAD_Chain_Link()
            cad_chain_link.CAD_Chain_Link_course = xml_chain_link.find("course").get("value")
            cad_chain_link.CAD_Chain_Link_layer = cad_layer
            cad_chain_link.save()

    print('Upload End')
    variables = {'success': True}
    return HttpResponse(variables)