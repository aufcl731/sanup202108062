import json
import requests

from django.contrib.auth.decorators import login_required
from django.core import serializers

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from order.models import *
from account.models import Company
from machine.models import Warp_Machine, Knit_Machine,YW_Knit_Machine, YW_Warp_Machine

# Create your views here.

def getWarpInfoByJson(request):
    id = int(request.POST['id'])
    type = int(request.POST['type'])

    if type == 1:
        warpMachineObj = Warp_Machine.objects.filter(pk=id)

        if warpMachineObj[0].tws_installation_time != None:
            installationTime = warpMachineObj[0].tws_installation_time.strftime('%Y-%m-%d %H:%M')
        else:
            installationTime = ''
        warpMachineObj = warpMachineObj.values()[0]
        warpMachineObj['tws_installation_time'] = installationTime
    else:
        warpMachineObj = YW_Warp_Machine.objects.filter(pk=id)

        if warpMachineObj[0].create_date != None:
            create_date = warpMachineObj[0].create_date.strftime('%Y-%m-%d %H:%M')
        else:
            create_date = ''

        companyName = warpMachineObj[0].company.name
        warpMachineObj = warpMachineObj.values()[0]
        warpMachineObj['create_date'] = create_date
        warpMachineObj['company_id'] = companyName

    print(warpMachineObj)

    return HttpResponse(json.dumps(warpMachineObj), content_type='application/json')

def getKnitInfoByJson(request):
    id = int(request.POST['id'])
    type = int(request.POST['type'])

    if type == 1:
        knitMachineObj = Knit_Machine.objects.filter(pk=id)

        if knitMachineObj[0].trs_installation_time != None:
            installationTime = knitMachineObj[0].trs_installation_time.strftime('%Y-%m-%d %H:%M')
        else:
            installationTime = ''
        knitMachineObj = knitMachineObj.values()[0]
        knitMachineObj['trs_installation_time'] = installationTime
    else:
        knitMachineObj = YW_Knit_Machine.objects.filter(pk=id)

        if knitMachineObj[0].create_data != None:
            create_data = knitMachineObj[0].create_data.strftime('%Y-%m-%d %H:%M')
        else:
            create_data = ''
        companyName = knitMachineObj[0].company.name
        knitMachineObj = knitMachineObj.values()[0]
        knitMachineObj['create_data'] = create_data
        knitMachineObj['company_id'] = companyName


    print(knitMachineObj)

    return HttpResponse(json.dumps(knitMachineObj), content_type='application/json')



@login_required(login_url='/')
def showMachine(request):

    company = Company.objects.get(id=1)

    if company.machineyn == True:
        jsonData = requests.get("http://tnswebserver.iptime.org:1978/values/trs").json()

        for trsObj in jsonData["trs"]:
            print(trsObj["tns_code"])

            if Knit_Machine.objects.filter(tns_code=trsObj["tns_code"]).count() == 0:
                trsMachineObj = Knit_Machine()
                trsMachineObj.tns_code = trsObj["tns_code"] if trsObj["tns_code"] != "" else None
                trsMachineObj.user_id = trsObj["user_id"] if trsObj["user_id"] != "" else None
                trsMachineObj.company_code = trsObj["company_code"] if trsObj["company_code"] != "" else None
                trsMachineObj.trs_installation_time = trsObj["trs_installation_time"] if trsObj[
                                                                                             "trs_installation_time"] != "" else None
                trsMachineObj.trs_model_name = trsObj["trs_model_name"] if trsObj["trs_model_name"] != "" else None
                trsMachineObj.trs_beam_cnt = trsObj["trs_beam_cnt"] if trsObj["trs_beam_cnt"] != "" else None
                trsMachineObj.trs_bar_cnt = trsObj["trs_bar_cnt"] if trsObj["trs_bar_cnt"] != "" else None
                trsMachineObj.trs_eac_enable = trsObj["trs_eac_enable"] if trsObj["trs_eac_enable"] != "" else None
                trsMachineObj.trs_tempo = trsObj["trs_tempo"] if trsObj["trs_tempo"] != "" else None
                trsMachineObj.trs_lowmotor_enable = trsObj["trs_lowmotor_enable"] if trsObj[
                                                                                         "trs_lowmotor_enable"] != "" else None
                trsMachineObj.trs_gauge = trsObj["trs_gauge"] if trsObj["trs_gauge"] != "" else None
                trsMachineObj.trs_ip = trsObj["trs_ip"] if trsObj["trs_ip"] != "" else None

                trsMachineObj.save()

        print("")

        jsonData = requests.get("http://tnswebserver.iptime.org:1978/values/tws").json()

        for tswObj in jsonData["tws"]:
            print(tswObj["tns_code"])

            if Warp_Machine.objects.filter(tns_code=tswObj["tns_code"]).count() == 0:
                trsMachineObj = Warp_Machine()
                trsMachineObj.tns_code = tswObj["tns_code"] if tswObj["tns_code"] != "" else None
                trsMachineObj.user_id = tswObj["user_id"] if tswObj["user_id"] != "" else None
                trsMachineObj.company_code = tswObj["company_code"] if tswObj["company_code"] != "" else None
                trsMachineObj.tws_name = tswObj["tws_name"] if tswObj["tws_name"] != "" else None
                trsMachineObj.tws_installation_time = tswObj["tws_installation_time"] if tswObj[
                                                                                             "tws_installation_time"] != "" else None
                trsMachineObj.tws_ip = tswObj["tws_ip"] if tswObj["tws_ip"] != "" else None

                trsMachineObj.save()

        warpMachineList = Warp_Machine.objects.all()
        knitMachineList = Knit_Machine.objects.all()
        orderList = Order.objects.all()

        variables = {'title': 'Machine', 'company': company, 'warpMachineList': warpMachineList, 'knitMachineList': knitMachineList,'orderList':orderList}
    else:
        warpMachineList = YW_Warp_Machine.objects.all()
        knitMachineList = YW_Knit_Machine.objects.all()
        orderList = Order.objects.all()

        variables = {'title': 'Machine', 'company': company, 'warpMachineList': warpMachineList, 'knitMachineList': knitMachineList,'orderList':orderList}

    return render(request, 'machine.html', variables)

def setWarpMachine(request):
    model = request.POST['warp_model']
    code = request.POST['warp_code']
    if model and code != '':
        company = Company.objects.get(id=1)

        print('model', model)
        print('code', code)

        warpMachinObj = YW_Warp_Machine(name=model, code=code, company=company)
        warpMachinObj.save()

        return redirect('/machine')
    else:
        msg = "정경기의 정보를 입력해주세요"
        return render(request, 'msg/errorPage.html', {'msg':msg})

def setKnitMachine(request):
    model = request.POST['knit_model']
    code = request.POST['knit_code']
    rpm = request.POST['knit_rpm']
    bar_cnt = request.POST['knit_bar_cnt']
    gauge = request.POST['knit_gauge']
    company = Company.objects.get(id=1)


    if model and code and rpm and bar_cnt and gauge !='':
        try:
            knitMachinObj = YW_Knit_Machine(name=model, code=code, company=company, rpm=rpm, gauge=gauge, bar_cnt=bar_cnt)
            knitMachinObj.save()

            return redirect('/machine')
        except ValueError:
            if bar_cnt.isdecimal() == False:
                msg = "Bar Count 에는 숫자만 입력 할 수 있습니다."
                return render(request, 'msg/errorPage.html', {'msg': msg})
            if rpm.isdecimal() == False:
                msg = "RPM 에는 숫자만 입력 할 수 있습니다."
                return render(request, 'msg/errorPage.html', {'msg':msg})
            if gauge.isdecimal() == False:
                msg = "Gauge 에는 숫자만 입력 할 수 있습니다."
                return render(request, 'msg/errorPage.html', {'msg': msg})
    else:
        msg = "경편기의 정보를 입력해주세요"
        return render(request, 'msg/errorPage.html', {'msg':msg})

def setMachine(request):
    jsonData = requests.get("http://tnswebserver.iptime.org:1978/values/trs").json()

    for trsObj in jsonData["trs"]:
        print(trsObj["tns_code"])

        if Knit_Machine.objects.filter(tns_code=trsObj["tns_code"]).count() == 0:
            trsMachineObj = Knit_Machine()
            trsMachineObj.tns_code = trsObj["tns_code"] if trsObj["tns_code"] != "" else None
            trsMachineObj.user_id = trsObj["user_id"] if trsObj["user_id"] != "" else None
            trsMachineObj.company_code = trsObj["company_code"] if trsObj["company_code"] != "" else None
            trsMachineObj.trs_installation_time = trsObj["trs_installation_time"] if trsObj["trs_installation_time"] != "" else None
            trsMachineObj.trs_model_name = trsObj["trs_model_name"] if trsObj["trs_model_name"] != "" else None
            trsMachineObj.trs_beam_cnt = trsObj["trs_beam_cnt"] if trsObj["trs_beam_cnt"] != "" else None
            trsMachineObj.trs_bar_cnt = trsObj["trs_bar_cnt"] if trsObj["trs_bar_cnt"] != "" else None
            trsMachineObj.trs_eac_enable = trsObj["trs_eac_enable"] if trsObj["trs_eac_enable"] != "" else None
            trsMachineObj.trs_tempo = trsObj["trs_tempo"] if trsObj["trs_tempo"] != "" else None
            trsMachineObj.trs_lowmotor_enable = trsObj["trs_lowmotor_enable"] if trsObj["trs_lowmotor_enable"] != "" else None
            trsMachineObj.trs_gauge = trsObj["trs_gauge"] if trsObj["trs_gauge"] != "" else None
            trsMachineObj.trs_ip = trsObj["trs_ip"] if trsObj["trs_ip"] != "" else None

            trsMachineObj.save()

    print("")

    jsonData = requests.get("http://tnswebserver.iptime.org:1978/values/tws").json()

    for tswObj in jsonData["tws"]:
        print(tswObj["tns_code"])

        if Warp_Machine.objects.filter(tns_code=tswObj["tns_code"]).count() == 0:
            trsMachineObj = Warp_Machine()
            trsMachineObj.tns_code = tswObj["tns_code"] if tswObj["tns_code"] != "" else None
            trsMachineObj.user_id = tswObj["user_id"] if tswObj["user_id"] != "" else None
            trsMachineObj.company_code = tswObj["company_code"] if tswObj["company_code"] != "" else None
            trsMachineObj.tws_name = tswObj["tws_name"] if tswObj["tws_name"] != "" else None
            trsMachineObj.tws_installation_time = tswObj["tws_installation_time"] if tswObj["tws_installation_time"] != "" else None
            trsMachineObj.tws_ip = tswObj["tws_ip"] if tswObj["tws_ip"] != "" else None

            trsMachineObj.save()

    return HttpResponse(json.dumps('{success: true}'), content_type='application/json')

@csrf_exempt
def listByType(request):

    machineType = int(request.POST['machineType'])

    if machineType == 1:
        machineList = Warp_Machine.objects.all()
    else:
        machineList = Knit_Machine.objects.all()

    jsonList = serializers.serialize('json', machineList)

    return HttpResponse(jsonList, content_type="text/json-comment-filtered")

@csrf_exempt
def deleteWarpMachine(request):
    type = int(request.POST['type'])
    id = int(request.POST['id'])

    if type == 2:
        warpMachineObj = YW_Warp_Machine.objects.get(id=id)
        warpMachineObj.delete()
    else:
        warpMachineObj = Warp_Machine.objects.get(id=id)
        warpMachineObj.delete()

    return redirect('/machine')

@csrf_exempt
def deleteKnitMachine(request):
    type = int(request.POST['type'])
    id = int(request.POST['id'])

    if type == 2:
        knitMachineObj = YW_Knit_Machine.objects.get(id=id)
        knitMachineObj.delete()
    else:
        knitMachineObj = Knit_Machine.objects.get(id=id)
        knitMachineObj.delete()

    return redirect('/machine')
