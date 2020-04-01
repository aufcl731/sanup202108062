import datetime
import json
import qrcode
import requests

from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from materials.models import *
from machine.models import *
from schedule.models import Knit_Process, Warp_Process, Warp_Beam, Knit_Beam
from order.models import *
from django.forms import model_to_dict
from design_data.models import *

@csrf_exempt
def selectOrder(request):
    orderId = int(request.POST['orderId'])
    type = int(request.POST['type'])

    designFabricObj = Order_DesignData.objects.get(pk=orderId).design_data_id.fsty_cad_production.fsty_cad_fabric_set.all()

    for obj in designFabricObj:
        if obj.CAD_Fabric_type == 'R':
            infoObj = obj

    if type == 1:
        twsJsonData = requests.get("http://tnswebserver.iptime.org:1978/values/tws").json()

        trsJsonData = requests.get("http://tnswebserver.iptime.org:1978/values/trs").json()


        for obj in twsJsonData['tws']:
            obj['id'] = Warp_Machine.objects.get(tns_code=obj['tns_code']).pk

        for obj in trsJsonData['trs']:
            obj['id'] = Knit_Machine.objects.get(tns_code=obj['tns_code']).pk
            obj['dailyOutPut'] = int(int(obj['trs_rpm_main']) * 24 * 60 / int(infoObj.CAD_Fabric_cpi) / 91.44 * int(infoObj.CAD_Fabric_width))

        machineJsonList = {'tws': twsJsonData['tws'], 'trs': trsJsonData['trs']}
    else:
        jsonKnitMachinList = []
        ywKnitMachineList = YW_Knit_Machine.objects.all()
        for obj in ywKnitMachineList:
            jsonKnitMachineObj = {}
            jsonKnitMachineObj['id'] = obj.pk
            jsonKnitMachineObj['dailyOutPut'] = int(int(obj.rpm) * 24 * 60 / int(infoObj.CAD_Fabric_cpi) / 91.44 * int(infoObj.CAD_Fabric_width))
            jsonKnitMachinList.append(jsonKnitMachineObj)

        machineJsonList = {'tws': [], 'trs': jsonKnitMachinList}

    desingYarnObj = Order_DesignData.objects.get(pk=orderId).design_data_id.fsty_cad_layer_set.all()

    yarnCodeList = []

    for obj in desingYarnObj:
        yarnCodeList.append(obj.fsty_cad_yarn.CAD_Yarn_code)

    yarnList = Yarn.objects.filter(code__in=yarnCodeList)
    beamList = Beam.objects.filter(yarn__in=yarnList)

    beamDictList = list(Beam.objects.filter(yarn__in=yarnList).values())
    for i, obj in enumerate(beamDictList):
        obj['yarnName'] = beamList[i].yarn.name

    print(beamList)

    return HttpResponse(json.dumps({'machineJsonList': machineJsonList, 'beamList': beamDictList, 'yarnList': list(yarnList.values())}), content_type='application/json')

@login_required
@csrf_exempt
def saveBeam(request):
    warpBeamId = request.POST.getlist('warpBeamId')
    warpYarn = request.POST.getlist('warpYarn')
    knitBeamId = request.POST.getlist('knitBeamId')
    designOrderId = request.POST['designOrderId']

    print('warpBeamId', warpBeamId)
    print('warpYarn', warpYarn)
    print('knitBeamId', knitBeamId)
    print('designId', designOrderId)

    warpBeamList = []
    try:
        for i in range(len(warpBeamId)):
            beam = Beam.objects.get(pk=int(warpBeamId[i]))
            warpProcess = Order_DesignData.objects.get(pk=int(designOrderId)).warp_process
            print('yarnId', int(warpYarn[i]))
            yarnObj = Yarn.objects.get(pk=int(warpYarn[i]))
            warpBeam = Warp_Beam(warp_process=warpProcess, beam=beam)
            warpBeam.save()
            beam.yarn = yarnObj
            beam.save()
            warpBeamList.append(warpBeam)
    except IndexError:
        msg = '비어있는 빔은 저장하실수 없습니다.'
        return render(request, 'msg/errorPage.html', {'msg': msg})

    for i in range(len(knitBeamId)):
        beam = Beam.objects.get(pk=int(knitBeamId[i]))
        knitProcess = Order_DesignData.objects.get(pk=int(designOrderId)).knit_process
        knitBeam = Knit_Beam(knit_process=knitProcess, beam=beam)
        knitBeam.save()

    for beamObj in warpBeamList:
        knitProcess = Order_DesignData.objects.get(pk=int(designOrderId)).knit_process
        knitBeam = Knit_Beam(knit_process=knitProcess, beam=beamObj.beam)
        knitBeam.save()

    return redirect('/production/process/'+designOrderId)

@login_required
@csrf_exempt
def showSchedule(request):
    designOrderList = Order_DesignData.objects.filter(warp_process__isnull=True, knit_process__isnull=True).order_by('-id')
    orderList = Order.objects.all()
    companyMachine = Company.objects.get(id=1)
    yarnList = Yarn.objects.all()

    if companyMachine.machineyn == True:
        warpMachineList = Warp_Machine.objects.all()
        knitMachineList = Knit_Machine.objects.all()
    else:
        warpMachineList = YW_Warp_Machine.objects.all()
        knitMachineList = YW_Knit_Machine.objects.all()


    return render(request, 'schedule.html', {'orderList' : orderList ,'title': 'Schedule', 'machine': companyMachine.machineyn, 'designOrderList': designOrderList, 'designOrderCount': designOrderList.count(), 'warpMachineList': warpMachineList, 'knitMachineList': knitMachineList, 'yarnList': yarnList})

@csrf_exempt
def getMachineByDate(request):
    year = int(request.POST['year'])
    month = int(request.POST['month'])
    date = int(request.POST['date'])
    type = int(request.POST['type'])

    endDate = datetime(year, month, date, int(23), int(59), int(59))
    startDate = datetime(year, month, date, int(0), int(0), int(0))

    if type == 1:
        warpProcessList = Warp_Process.objects.filter(end_time__gte=startDate, end_time__lte=endDate, yw_warp_machine_id__isnull=True) | Warp_Process.objects.filter(start_time__gte=startDate, start_time__lte=endDate, yw_warp_machine_id__isnull=True) | Warp_Process.objects.filter(end_time__gt=endDate, start_time__lt=startDate, yw_warp_machine_id__isnull=True)
        warpProcessJsonList = []
        for warpProcessObj in warpProcessList:
            jsonOrderObj = {}
            jsonOrderObj['order'] = warpProcessObj.order_designdata.code
            jsonOrderObj['warpMachine'] = warpProcessObj.warp_machine_id.tns_code
            jsonOrderObj['startTime'] = warpProcessObj.start_time.strftime("%Y-%m-%d %H:%M")
            jsonOrderObj['endTime'] = warpProcessObj.end_time.strftime("%Y-%m-%d %H:%M")

            warpProcessJsonList.append(jsonOrderObj)

        knitProcessList = Knit_Process.objects.filter(end_time__gte=startDate, end_time__lte=endDate, yw_knit_machine_id__isnull=True) | Knit_Process.objects.filter(start_time__gte=startDate, start_time__lte=endDate, yw_knit_machine_id__isnull=True) | Knit_Process.objects.filter(end_time__gt=endDate, start_time__lt=startDate, yw_knit_machine_id__isnull=True)
        knitProcessJsonList = []
        for knitProcessObj in knitProcessList:
            jsonOrderObj = {}
            jsonOrderObj['order'] = knitProcessObj.order_designdata.code
            jsonOrderObj['knitMachine'] = knitProcessObj.knit_machine_id.tns_code
            jsonOrderObj['startTime'] = knitProcessObj.start_time.strftime("%Y-%m-%d %H:%M")
            jsonOrderObj['endTime'] = knitProcessObj.end_time.strftime("%Y-%m-%d %H:%M")

            knitProcessJsonList.append(jsonOrderObj)
    else:
        warpProcessList = Warp_Process.objects.filter(end_time__gte=startDate, end_time__lte=endDate, yw_warp_machine_id__isnull=False) | Warp_Process.objects.filter(start_time__gte=startDate, start_time__lte=endDate, yw_warp_machine_id__isnull=False) | Warp_Process.objects.filter(end_time__gt=endDate, start_time__lt=startDate, yw_warp_machine_id__isnull=False)
        warpProcessJsonList = []
        for warpProcessObj in warpProcessList:
            jsonOrderObj = {}
            jsonOrderObj['order'] = warpProcessObj.order_designdata.code
            jsonOrderObj['warpMachine'] = warpProcessObj.yw_warp_machine_id.code
            jsonOrderObj['startTime'] = warpProcessObj.start_time.strftime("%Y-%m-%d %H:%M")
            jsonOrderObj['endTime'] = warpProcessObj.end_time.strftime("%Y-%m-%d %H:%M")

            warpProcessJsonList.append(jsonOrderObj)

        knitProcessList = Knit_Process.objects.filter(end_time__gte=startDate, end_time__lte=endDate, yw_knit_machine_id__isnull=False) | Knit_Process.objects.filter(start_time__gte=startDate, start_time__lte=endDate, yw_knit_machine_id__isnull=False) | Knit_Process.objects.filter(end_time__gt=endDate, start_time__lt=startDate, yw_knit_machine_id__isnull=False)
        knitProcessJsonList = []
        for knitProcessObj in knitProcessList:
            jsonOrderObj = {}
            jsonOrderObj['order'] = knitProcessObj.order_designdata.code
            jsonOrderObj['knitMachine'] = knitProcessObj.yw_knit_machine_id.code
            jsonOrderObj['startTime'] = knitProcessObj.start_time.strftime("%Y-%m-%d %H:%M")
            jsonOrderObj['endTime'] = knitProcessObj.end_time.strftime("%Y-%m-%d %H:%M")

            knitProcessJsonList.append(jsonOrderObj)

    variable = {'knitProcessList': knitProcessJsonList, 'warpProcessList': warpProcessJsonList}

    return HttpResponse(json.dumps(variable), content_type='application/json')

@csrf_exempt
def getMaterialByJson(request):
    type = int(request.POST['type'])

    if type == 1:
        materialList = Yarn.objects.all()
    elif type == 2:
        materialList = Beam.objects.all()
    else:
        materialList = Raw.objects.all()

    return HttpResponse(json.dumps({'materialList': materialList}), content_type='application/json')


@csrf_exempt
def getProcessByJson(request):
    year = int(request.POST['year'])
    month = int(request.POST['month'])
    date = int(request.POST['date'])
    warpMachine = request.POST.get('warpMachine', None)
    knitMachine = request.POST.get('knitMachine', None)

    endDate = datetime.datetime(year, month, date, 23, 59, 59)
    startDate = datetime.datetime(year, month, date, 0, 0, 0)
    print(endDate)
    print(startDate)


    if warpMachine != None:
        warpMachineObj = Warp_Machine.objects.get(pk=warpMachine)
        warpProcessList = Warp_Process.objects.filter(warp_machine_id=warpMachineObj, end_time__gte=startDate, end_time__lte=endDate) | Warp_Process.objects.filter(warp_machine_id=warpMachineObj, start_time__gte=startDate, start_time__lte=endDate) | Warp_Process.objects.filter(warp_machine_id=warpMachineObj, end_time__gt=endDate, start_time__lt=startDate)
        warpProcessJsonList = []
        for warpProcessObj in warpProcessList:
            jsonOrderObj = {}
            jsonOrderObj['order'] = warpProcessObj.order_designdata.code
            jsonOrderObj['startTime'] = warpProcessObj.start_time.strftime("%Y-%m-%d %H:%M")
            jsonOrderObj['endTime'] = warpProcessObj.end_time.strftime("%Y-%m-%d %H:%M")

            warpProcessJsonList.append(jsonOrderObj)

        variable = {'success': True, 'processList': warpProcessJsonList}
    else:
        knitMachineObj = Knit_Machine.objects.get(pk=knitMachine)
        knitProcessList = Knit_Process.objects.filter(knit_machine_id=knitMachineObj, end_time__gte=startDate, end_time__lte=endDate) | Knit_Process.objects.filter(knit_machine_id=knitMachineObj, start_time__gte=startDate, start_time__lte=endDate) | Knit_Process.objects.filter(knit_machine_id=knitMachineObj, end_time__gt=endDate, start_time__lt=startDate)
        knitProcessJsonList = []
        for knitProcessObj in knitProcessList:
            jsonOrderObj = {}
            jsonOrderObj['order'] = knitProcessObj.order_designdata.code
            jsonOrderObj['startTime'] = knitProcessObj.start_time.strftime("%Y-%m-%d %H:%M")
            jsonOrderObj['endTime'] = knitProcessObj.end_time.strftime("%Y-%m-%d %H:%M")

            knitProcessJsonList.append(jsonOrderObj)

        variable = {'success': True, 'processList': knitProcessJsonList}

    return HttpResponse(json.dumps(variable), content_type='application/json')


@csrf_exempt
def createSchedule(request):
    try:
        orderId = int(float(request.POST['orderId']))
        warpMachineId = int(request.POST['warpMachineId'])
        warpingStart = request.POST['warpStartTime']
        warpingEnd = request.POST['warpEndTime']
        knitMachineId = int(request.POST['knitMachineId'])
        knitingStart = request.POST['knitStartTime']
        knitingEnd = request.POST['knitEndTime']
        machine = int(request.POST['machine'])

        oerder_designObj = Order_DesignData.objects.get(id=orderId)

        if machine == 1:
            warpMachineObj = Warp_Machine.objects.get(id=warpMachineId)
            warpProcessObj = Warp_Process(order_designdata=oerder_designObj, warp_machine_id=warpMachineObj, start_time=warpingStart, end_time=warpingEnd)
            warpProcessObj.save()

            knitMachineObj = Knit_Machine.objects.get(id=knitMachineId)
            knitProcessObj = Knit_Process(order_designdata=oerder_designObj, knit_machine_id=knitMachineObj, start_time=knitingStart, end_time=knitingEnd)
            knitProcessObj.save()
        else:
            warpMachineObj = YW_Warp_Machine.objects.get(id=warpMachineId)
            warpProcessObj = Warp_Process(order_designdata=oerder_designObj, yw_warp_machine_id=warpMachineObj, start_time=warpingStart, end_time=warpingEnd)
            warpProcessObj.save()

            knitMachineObj = YW_Knit_Machine.objects.get(id=knitMachineId)
            knitProcessObj = Knit_Process(order_designdata=oerder_designObj, yw_knit_machine_id=knitMachineObj, start_time=knitingStart, end_time=knitingEnd)
            knitProcessObj.save()

        domain = request.get_host()
        scheme = request.is_secure() and "https" or "http"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=6,
            border=0,
        )

        domain = request.get_host()
        scheme = request.is_secure() and "https" or "http"

        jsonSubOrderObj = {}

        jsonSubOrderObj['Ordername'] = oerder_designObj.code
        jsonSubOrderObj['buyer'] = oerder_designObj.order_id.buyer
        jsonSubOrderObj['order_date'] = oerder_designObj.order_id.order_date.strftime("%Y-%m-%d")
        jsonSubOrderObj['due_date'] = oerder_designObj.order_id.due_date.strftime("%Y-%m-%d")
        jsonSubOrderObj['designData'] = oerder_designObj.design_data_id.CAD_Design_Data_code
        jsonSubOrderObj['link'] = scheme + '://' + domain + '/order/subOrderJson/' + str(orderId)


        qr.add_data(str(json.dumps(jsonSubOrderObj)))
        qr.make()
        qr_code_image = qr.make_image()
        buffer = BytesIO()
        qr_code_image.save(buffer)
        print('qr End')
        filebuffer = InMemoryUploadedFile(buffer, None, 'qr_code_image.png', 'image/png', buffer.getbuffer().nbytes, None)

        qr_code_image_path = 'data/qrcode/' + str(orderId) + '/qr_code_image.png'
        oerder_designObj.qr_code.save(qr_code_image_path, filebuffer)

        return redirect('/schedule')
    except ValueError:
        msg = '스케쥴정보를 입력해주세요'
        return render(request, 'msg/errorPage.html', {'msg': msg})
