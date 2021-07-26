import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
import requests

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from account.models import Company
from order.models import *
from schedule.models import Knit_Process, Warp_Process, Knit_Machine_Realtime, Warp_Machine_Realtime, Warp_Beam, Knit_Beam
from materials.models import Beam, Yarn


@csrf_exempt
@login_required(login_url='/')
def showDesignProduction(request, productionId):

    orderObj = Order_DesignData.objects.get(pk=productionId)
    designObj = orderObj.design_data_id

    return render(request, 'worksheet/knit.html', {'object': designObj, 'qrCode':orderObj.qr_code, 'orderQty':orderObj.design_qty, 'userlang':request.user})


def production(request):

    title = 'Production'
    orderList = Order.objects.all()
    designOrderList = Order_DesignData.objects.all().order_by('-id')

    order = []

    for designOrder in designOrderList:
        try:
            wProcess = Warp_Process.objects.get(order_designdata=designOrder)
            wSchedule = True
        except:
            wSchedule = False

        try:
            kProcess = Knit_Process.objects.get(order_designdata=designOrder)
            kSchedule = True
            #kRealTime = Knit_Machine_Realtime.objects.get(knit_process=kProcess)

            jsonData = requests.get("http://tnswebserver.iptime.org:1978/api/trs").json()
            for obj in jsonData['trs']:
                if obj['tns_code'] == kProcess.knit_machine_id.tns_code:
                    designOrder.trs_total_meter = obj['trs_meter']
        except:
            kSchedule = False

        if kSchedule | wSchedule:
            order.append(designOrder)


    return render(request, 'production.html', {'title':title, 'designOrderList':order, 'orderList':orderList, 'userlang':request.user})



def productionDetail(request, pk):

    companyMachine = Company.objects.get(id=1)
    designOrder = Order_DesignData.objects.get(id=pk)
    kMachine = {}
    wMachine = {}
    if companyMachine.machineyn == True:

        wProcess = Warp_Process.objects.get(order_designdata=pk)

        if Warp_Beam.objects.filter(warp_process=wProcess).count() > 0:
            wSchedule = True
            #wRealTime = Warp_Machine_Realtime.objects.get(knit_process=wProcess)
            jsonData = requests.get("http://tnswebserver.iptime.org:1978/api/tws").json()
            for obj in jsonData['tws']:
                try:
                    if obj['tns_code'] == wProcess.warp_machine_id.tns_code:
                        wMachine = obj
                except AttributeError:
                    msg = '받아오는 기계 정보가 없습니다.'
                    return render(request, 'msg/errorPage.html', {'msg': msg})
            kProcess = Knit_Process.objects.get(order_designdata=pk)
            kSchedule = True
            #kRealTime = Knit_Machine_Realtime.objects.get(knit_process=kProcess)
            jsonData = requests.get("http://tnswebserver.iptime.org:1978/api/trs").json()
            for obj in jsonData['trs']:
                if obj['tns_code'] == kProcess.knit_machine_id.tns_code:
                    kMachine = obj

            designFabricObj = designOrder.design_data_id.fsty_cad_production.fsty_cad_fabric_set.all()
            for obj in designFabricObj:
                if obj.CAD_Fabric_type == 'R':
                    infoObj = obj
            try:
                if int(kMachine['trs_rpm_main']) != 0:
                    kMachine['dailyOutPut'] = int(
                        int(kMachine['trs_rpm_main']) * 24 * 60 / int(infoObj.CAD_Fabric_cpi) / 91.44 * int(
                            infoObj.CAD_Fabric_width))

                    outputPerMin = kMachine['dailyOutPut'] / 24 / 60

                    kMachine['trs_meter'] = int(kMachine['trs_meter'])

                    kMachine['lostMin'] = int((designOrder.design_qty - kMachine['trs_meter']) / outputPerMin)

                    kMachine['lostHour'] = kMachine['lostMin'] // 60

                    kMachine['lostMin'] = kMachine['lostMin'] % 60

                    warp_Beam = Warp_Beam.objects.filter(warp_process=wProcess)
                    knit_Beam = Knit_Beam.objects.filter(knit_process=kProcess)
                else:
                    kMachine['dailyOutPut'] = 0

                    outputPerMin = kMachine['dailyOutPut'] / 24 / 60

                    kMachine['trs_meter'] = int(kMachine['trs_meter'])

                    kMachine['lostMin'] = 0

                    kMachine['lostHour'] = kMachine['lostMin'] // 60

                    kMachine['lostMin'] = kMachine['lostMin'] % 60

                    warp_Beam = Warp_Beam.objects.filter(warp_process=wProcess)
                    knit_Beam = Knit_Beam.objects.filter(knit_process=kProcess)
            except:
                msg = '기계가 가동 중이지 않습니다.'
                return render(request, 'msg/errorPage.html', {'msg': msg})

            variables = {'title':'Production', 'designOrder':designOrder, 'knit_Beam':knit_Beam, 'warp_Beam':warp_Beam, 'kSchedule':kSchedule, 'wSchedule':wSchedule, 'wProcess':wProcess, 'kProcess':kProcess, 'kMachine':kMachine, 'wMachine':wMachine, 'cpi':infoObj.CAD_Fabric_cpi, 'width':infoObj.CAD_Fabric_width}
        else:
            beamList = Beam.objects.all()
            kSchedule = False
            wSchedule = False

            desingYarnList = designOrder.design_data_id.fsty_cad_layer_set.all()

            yarnCodeList = []

            for obj in desingYarnList:
                yarnCodeList.append(obj.fsty_cad_yarn.CAD_Yarn_code)

            yarnJsonList = []

            yarnList = Yarn.objects.filter(code__in=yarnCodeList)

            for obj in yarnList:
                yarnJsonList.append({'pk': obj.pk, 'code': obj.code})

            variables = {'title':'Production', 'designOrder':designOrder, 'kSchedule':kSchedule, 'wSchedule':wSchedule, 'beamList': beamList, 'totalBeamCount': beamList.count(), 'desingYarnList': yarnJsonList}

        return render(request, 'productionDetail.html', variables)
    else:

        variables = {'title':'Production', 'designOrder':designOrder}

        return render(request, 'productionNoMachine.html', variables)


def setOrders(request):
    try:
        warptopJSON = requests.get("http://tnswebserver.iptime.org:1978/api/tws_chart").json()
    except Exception as e:
        print(e)

    return HttpResponse(json.dump({'success':True}),content_type='applications')