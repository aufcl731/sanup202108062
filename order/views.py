import binascii
import datetime
import json
import os
import string

import requests
from django.contrib.auth.decorators import login_required
from requests_toolbelt.multipart.encoder import MultipartEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from datetime import datetime
from account.models import *
from design_data.models import *
from order.models import *
from order.models import Order, Order_DesignData
from .serializer import *
from materials.models import *


# order 등록수정해야 할점 시간이 무조건 15:00 로 들어감. html order_date 를 disabled 하고 현재시간으로 세팅하는게 바람직해보임.

@login_required(login_url='/')
def order(request):

    title = 'Order'

    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c'
    }
    #주문자 연계 시스템 스타일 오더정보
    jsonData = requests.get("http://api.lookiss.com:9403/api/SCC/GetStyleFabrics", headers=headers)
    data = json.loads(jsonData.text)
    print("주문자 연계 시스템 스타일 오더정보data : ",data)
    for styleObj in data:
        for obj in styleObj['fabrics']:
            print("styleObj['styleKey'] :", styleObj['styleKey'])
            changeStyleck(styleObj['styleKey'])
    try:
        for styleObj in data:
            for obj in styleObj['fabrics']:
                st_fairic = Style_fabric.objects.create(fabric_code=obj['fabricCode'], fabric_name=obj['fabricName'],
                                                        fabric_color=obj['fabricColor'], fabric_size=obj['fabricSize'],
                                                        fabric_part=obj['fabricPart'], fabric_Construction=obj['fabricConstruction'],
                                                        fabric_width=obj['fabricWidth'], cuttable_width=obj['cuttableWidth'],
                                                        sMeter_width=obj['sMeterWeight'], yard_weight=obj['yardWeight'], unit=obj['unit'],
                                                        fabric_Csm=obj['fabricCsm'],
                                                        fabric_Mrp=obj['fabricMrp'], dyeProcessTypeCode=obj['dyeProcessTypeCode'],
                                                        dyeProcessTypeName=obj['dyeProcessTypeName'], dyeCompanyName=obj['dyeCompanyName'],
                                                        knitCompanyName=obj['knitCompanyName'], dyeCompanyCode=obj['dyeCompanyCode'],
                                                        knitCompanyCode=obj['knitCompanyCode'], FabricLoss=obj['fabricLoss'],
                                                        FabricCsm=obj['fabricCsm'])
                st_fairic.save()
                st_order = Style_orders.objects.create(style_key=styleObj['styleKey'], factory_code=styleObj['factoryCode'],
                                                       style_ver=styleObj['styleFabricVersion'], fabric_info=st_fairic,
                                                       factory_name=styleObj['factoryName'])
                st_order.save()
                if obj['yarns'] != '':
                    for yarn_obj in obj['yarns']:
                        style_fabric = Style_fabric.objects.get(fabric_code=obj['fabricCode'])
                        st_yarn = Style_yarn.objects.create(st_yarn_code=yarn_obj['yarnCode'], st_yarn_name=yarn_obj['yarnName'], st_yarn_color=yarn_obj['yarnColor'], st_yarn_rate=yarn_obj['contentRate'],
                                                            st_yarn_cnt=yarn_obj['yarnCount'], yn_Dye=yarn_obj['ynDye'])
                        st_yarn.save()
                        style_fabric.yarn = st_yarn
                        style_fabric.save()
                        print("스타일 페브릭 :", style_fabric)


    except Exception as e:
        print("error : ",e)
        pass

    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c'
    }
    #편직 생산 의뢰
    jsonData = requests.get("http://api.lookiss.com:9403/api/SCC/GetKnitWorks", headers=headers)
    print("편직 생산 의뢰:", jsonData.status_code)
    data = json.loads(jsonData.text)
    print("편직 생산 의뢰data: ", data )
    try:
        for orderObj in data:
            try:
                manage = Account.objects.get(accountname=orderObj['customerName'], accountmanager=orderObj['customerUser'])
                manage2 = Account.objects.get(accountname=orderObj['customerName'], accountmanager=orderObj['customerUser'],
                                                accounttype=orderObj['customerCode'], accountnum=orderObj['customerTel'],
                                                accountaddress=orderObj['customerAddress'])
                print("manage2 :", manage2)
            except ObjectDoesNotExist:
                # if orderObj['customerUser'] is None or orderObj['customerUser'] == '':
                #     orderObj['customerUser'] = 'None'
                manage = Account.objects.create(accountname=orderObj['customerName'], accountmanager=orderObj['customerUser'],
                                                accounttype=orderObj['customerCode'], accountwork='트리코드', accountnum=orderObj['customerTel'],
                                                accountaddress=orderObj['customerAddress'])
                print("저장 어카우느 없을때")
                manage.save()
            print("편직생산의뢰 저장 ", orderObj['knitWorkKey'])
            # print("stylekey :", orderObj['styleKey'])
            knitWorkKey = orderObj['knitWorkKey']
            for i, orders in enumerate(orderObj['items']):
                order_date_c = orderObj['workDate']
                due_date_c = orderObj['expectedDate']
                try:
                    new_order = Order.objects.get(code=orders['styleKey'])
                    print("stylekey :", new_order.code)
                    print("new Order :", new_order.knitWorkKey)
                except ObjectDoesNotExist:
                    try:
                        fabric = FSTY_CAD_Design_Data.objects.get(CAD_Design_Data_code='YW-TENSION')
                        order_date = datetime.strptime(order_date_c, '%Y-%m-%d')
                        due_date = datetime.strptime(due_date_c, '%Y-%m-%d')
                        new_order = Order.objects.create(code=orders['styleKey'], company=request.user.username, buyer=manage.pk,
                                                         type=0, state=0, order_date=order_date, due_date=due_date,
                                                         order_round=1, order_inout=1, cheack=False, manager=request.user, value=True, knitWorkKey=knitWorkKey)
                        print("new_order save",new_order)
                        new_order.save()
                        print('dddssss')
                        try:
                            new_order_de = Order_DesignData.objects.create(code=new_order.code, design_qty=orders['knitQty'],
                                                                   qr_code='', design_data_id=fabric ,order_id=new_order)#, knitWorkKey=orders['knitWorkKey'])
                            print("new_order save", new_order_de)
                            new_order_de.save()
                            print("new_order_de",new_order_de)
                        except Exception as e:
                            print("error: ", e)
                    except Exception as e:
                        print("error: ", e)
                        print('해당 원단 없음')
                        pass
    except Exception as e:
        print("error :", e)
        pass
    myCompany = Company.objects.get(id=1)
    if request.method == 'POST':
        company = request.POST['company']
        buyer = request.POST['buyer']
        #username = request.POST['username']
        #order_date_str = request.POST['order_date']
        order_type = request.POST['order_type']
        order_inout = request.POST['order_inout']
        order_round = request.POST['order_round']
        due_date_str = request.POST['due_date']
        designQty = request.POST.getlist('designQty')
        designID = request.POST.getlist('designID')

        #print(order_date_str)
        # html input type=date 를 받아오면 문자열로 받아옴. date 로 변환
        #order_date = datetime.datetime.strptime(order_date_str, '%Y-%m-%d').date()

        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        order_date = timezone.localtime()



        #Updated upstream
        # 오더코드 = 현재시간 + 오더타입 + 오더인아웃
        order_code = datetime.today().strftime("%Y%m%d%H%M%S")[2:] + str(order_type) + str(order_inout)
        # 오덬코드 = 현재시간(-20) + 오더타입 + 오더인아웃 + 차수
        #order_code = datetime.datetime.today().strftime("%Y%m%d%H%M%S")[2:] + str(order_type) + str(order_inout) + str(order_round)

        order = Order(company=company, manager=request.user, code=order_code, buyer=buyer, type=order_type, state=0, order_date=order_date, due_date=due_date, order_inout=order_inout, order_round=order_round)
        order.save()

        # 오더 디자인데이터 저장
        for i in range(len(designID)):
            design_data = FSTY_CAD_Design_Data(CAD_Design_Data_id=int(designID[i]))
            designOrder = Order_DesignData(order_id=order, code=order_code+"-"+str(i+1), design_data_id=design_data, design_qty=int(designQty[i]))
            designOrder.save()

        return redirect('/order')

    orderList = Order.objects.all().order_by('-id')
    designList = FSTY_CAD_Design_Data.objects.all().order_by("-CAD_Design_Data_id")
    accountList = Account.objects.all()
    style_order = Style_orders.objects.all()
    # oid=Order_DesignData.order_id
    # print("oid :",oid)
    # # changeStyleck()
    return render(request, 'order.html', {'title':title, 'designCount':designList.count(), 'orderCount':orderList.count(),
                                          'designDataList': designList, 'orderList': orderList, 'company': myCompany.name,
                                          'accountList':accountList,'userlang':request.user,'style_order':style_order})

@csrf_exempt
def changeStyleck(StyleKey):
    print("ordercheck?",StyleKey)
    # style_order = Style_orders.objects.get(pk=orderId)
    jsonobj = {}
    # jsonobj['StyleKey'] = style_order.style_key
    jsonobj['StyleKey'] = StyleKey
    jsonobj['Status'] = 'KNITRCV'
    content = json.dumps(jsonobj)
    headers = {
        'Content-Type': "application/json",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c',
    }
    print("content : ", content)
    style_ck = requests.post('http://api.lookiss.com:9403/api/SCC/ChangeStyleStatus', headers=headers,
                             data=content)
    print("스타일 개발의뢰 원단 정보 확인 요청 접수 :", style_ck.status_code)
    return HttpResponse(json.dumps(jsonobj), content_type='application/json')

@csrf_exempt
def ordercheack(request):

    if request.method == 'POST':
        oid = request.POST['oid']
        ordercheack = True
        order = Order.objects.get(id=oid)
        order.cheack = ordercheack
        order.save()

        return render(request, 'order.html', {})

@csrf_exempt
def getOrderListByJson(request):
    jsonOrderList = []
    orderList = Order.objects.all()

    for orderObj in orderList:
        jsonOrderObj = {}
        jsonOrderObj['orderId'] = orderObj.id
        jsonOrderObj['company'] = orderObj.company
        jsonOrderObj['manager'] = orderObj.manager.name
        jsonOrderObj['code'] = orderObj.code
        jsonOrderObj['buyer'] = orderObj.buyer
        jsonOrderObj['type'] = orderObj.type
        jsonOrderObj['state'] = orderObj.state
        jsonOrderObj['order_date'] = orderObj.order_date.strftime("%Y-%m-%d")
        jsonOrderObj['due_date'] = orderObj.due_date.strftime("%Y-%m-%d")
        jsonOrderObj['order_round'] = orderObj.order_round
        jsonOrderObj['order_inout'] = orderObj.order_inout

        jsonOrderList.append(jsonOrderObj)

    return HttpResponse(json.dumps({'orderList': jsonOrderList}), content_type='application/json')

@csrf_exempt
def showQr(request, id):
    return render(request, 'showQr.html', {'id':id})

@csrf_exempt
def getSubOrderByJson(request, id):
    subOrderObj = Order_DesignData.objects.get(id=id)
    jsonSubOrderObj = {}
    jsonSubOrderObj['code'] = subOrderObj.code
    jsonSubOrderObj['design_qty'] = subOrderObj.design_qty
    if subOrderObj.qr_code == '' or subOrderObj.qr_code == None:
        jsonSubOrderObj['qr_code'] = None
    else:
        jsonSubOrderObj['qr_code'] = subOrderObj.qr_code.url

    jsonDesignObj = {}

    layerList = FSTY_CAD_Layer.objects.filter(CAD_Layer_design_data=subOrderObj.design_data_id)
    fabricList = FSTY_CAD_Fabric.objects.filter(CAD_Fabric_production=subOrderObj.design_data_id.fsty_cad_production)

    jsonFabricList = []
    for fabricObj in fabricList:
        jsonFabricObj = {}
        jsonFabricObj['Fabric_id'] = fabricObj.CAD_Fabric_id
        jsonFabricObj['Fabric_type'] = fabricObj.CAD_Fabric_type
        jsonFabricObj['Fabric_wpi'] = fabricObj.CAD_Fabric_wpi
        jsonFabricObj['Fabric_cpi'] = fabricObj.CAD_Fabric_cpi
        jsonFabricObj['Fabric_width'] = fabricObj.CAD_Fabric_width
        jsonFabricObj['Fabric_weight_per_width'] = fabricObj.CAD_Fabric_weight_per_width
        jsonFabricList.append(jsonFabricObj)

    jsonLayerList = []
    for layerObj in layerList:
        jsonLayerObj = {}
        jsonLayerObj['Layer_id'] = layerObj.CAD_Layer_id
        jsonLayerObj['Layer_name'] = layerObj.CAD_Layer_name
        jsonLayerObj['Layer_ratio'] = layerObj.CAD_Layer_ratio
        jsonLayerObj['Layer_mm_rack'] = layerObj.CAD_Layer_mm_rack
        jsonLayerObj['Layer_use'] = layerObj.CAD_Layer_use
        jsonLayerObj['Layer_beam'] = layerObj.CAD_Layer_beam
        jsonLayerObj['Layer_total'] = layerObj.CAD_Layer_total
        jsonLayerObj['Layer_iodata'] = layerObj.CAD_Layer_iodata
        jsonLayerObj['Yarn'] = {}
        jsonLayerObj['Yarn']['id'] = layerObj.fsty_cad_yarn.CAD_Yarn_id
        jsonLayerObj['Yarn']['idx'] = layerObj.fsty_cad_yarn.CAD_Yarn_idx
        jsonLayerObj['Yarn']['maker'] = layerObj.fsty_cad_yarn.CAD_Yarn_maker
        jsonLayerObj['Yarn']['spec'] = layerObj.fsty_cad_yarn.CAD_Yarn_spec
        jsonLayerObj['Yarn']['code'] = layerObj.fsty_cad_yarn.CAD_Yarn_code
        jsonLayerObj['Yarn']['rgb_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_rgb_color
        jsonLayerObj['Yarn']['lab_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_lab_color
        jsonLayerObj['Yarn']['pantone_color'] = layerObj.fsty_cad_yarn.CAD_Yarn_pantone_color
        jsonLayerObj['Chain_Link'] = {}
        jsonLayerObj['Chain_Link']['id'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_id
        jsonLayerObj['Chain_Link']['course'] = layerObj.fsty_cad_chain_link.CAD_Chain_Link_course
        jsonLayerList.append(jsonLayerObj)
    jsonDesignObj['Design_Data_id'] = subOrderObj.design_data_id.CAD_Design_Data_id
    jsonDesignObj['Design_Data_name'] = subOrderObj.design_data_id.CAD_Design_Data_name
    jsonDesignObj['Design_Data_code'] = subOrderObj.design_data_id.CAD_Design_Data_code
    jsonDesignObj['Design_Data_pattern_image'] = subOrderObj.design_data_id.CAD_Design_Data_pattern_image.url
    jsonDesignObj['Design_Data_simulation_image'] = subOrderObj.design_data_id.CAD_Design_Data_simulation_image.url
    jsonDesignObj['Design_Data_create_date'] = subOrderObj.design_data_id.CAD_Design_Data_create_date.strftime("%Y-%m-%d")
    jsonDesignObj['Design_Data_magnification'] = subOrderObj.design_data_id.CAD_Design_Data_magnification
    jsonDesignObj['Production'] = {}
    jsonDesignObj['Production']['id'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_id
    jsonDesignObj['Production']['quota_per_day'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_quota_per_day
    jsonDesignObj['Production']['machine_name'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_machine_name
    jsonDesignObj['Production']['note'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_note
    jsonDesignObj['Production']['Fabric'] = jsonFabricList
    jsonDesignObj['Layer'] = jsonLayerList

    jsonSubOrderObj['design_data'] = jsonDesignObj

    return HttpResponse(json.dumps(jsonSubOrderObj), content_type='application/json')
@csrf_exempt
def getOrderByJson(request, orderId):

    jsonOrderObj = {}

    if orderId != None:
        orderObj = Order.objects.get(id=orderId)
        jsonOrderObj['company'] = orderObj.company
        jsonOrderObj['manager'] = orderObj.manager.name
        jsonOrderObj['code'] = orderObj.code
        jsonOrderObj['buyer'] = orderObj.buyer
        jsonOrderObj['type'] = orderObj.type
        jsonOrderObj['state'] = orderObj.state
        jsonOrderObj['order_date'] = orderObj.order_date.strftime("%Y-%m-%d")
        jsonOrderObj['due_date'] = orderObj.due_date.strftime("%Y-%m-%d")
        jsonOrderObj['order_round'] = orderObj.order_round
        jsonOrderObj['order_inout'] = orderObj.order_inout

        subOrderList = Order_DesignData.objects.filter(order_id=orderObj)

        jsonSubOrderList = []

        for subOrderObj in subOrderList:
            jsonSubOrderObj = {}
            jsonSubOrderObj['code'] = subOrderObj.code
            jsonSubOrderObj['design_qty'] = subOrderObj.design_qty
            if subOrderObj.qr_code == '' or subOrderObj.qr_code == None:
                jsonSubOrderObj['qr_code'] = None
            else:
                jsonSubOrderObj['qr_code'] = subOrderObj.qr_code.url

            jsonDesignObj = {}

            layerList = FSTY_CAD_Layer.objects.filter(CAD_Layer_design_data=subOrderObj.design_data_id)
            fabricList = FSTY_CAD_Fabric.objects.filter(CAD_Fabric_production=subOrderObj.design_data_id.fsty_cad_production)

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

            jsonDesignObj['CAD_Design_Data_id'] = subOrderObj.design_data_id.CAD_Design_Data_id
            jsonDesignObj['CAD_Design_Data_name'] = subOrderObj.design_data_id.CAD_Design_Data_name
            jsonDesignObj['CAD_Design_Data_code'] = subOrderObj.design_data_id.CAD_Design_Data_code
            jsonDesignObj['CAD_Design_Data_pattern_image'] = subOrderObj.design_data_id.CAD_Design_Data_pattern_image.url
            jsonDesignObj['CAD_Design_Data_simulation_image'] = subOrderObj.design_data_id.CAD_Design_Data_simulation_image.url
            jsonDesignObj['CAD_Design_Data_create_date'] = subOrderObj.design_data_id.CAD_Design_Data_create_date.strftime("%Y-%m-%d")
            jsonDesignObj['CAD_Design_Data_magnification'] = subOrderObj.design_data_id.CAD_Design_Data_magnification
            jsonDesignObj['FSTY_CAD_Production'] = {}
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_id'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_id
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_quota_per_day'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_quota_per_day
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_machine_name'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_machine_name
            jsonDesignObj['FSTY_CAD_Production']['CAD_Production_note'] = subOrderObj.design_data_id.fsty_cad_production.CAD_Production_note
            jsonDesignObj['FSTY_CAD_Production']['FSTY_CAD_Fabric'] = jsonFabricList
            jsonDesignObj['FSTY_CAD_Layer'] = jsonLayerList

            jsonSubOrderObj['design_data'] = jsonDesignObj

            jsonSubOrderList.append(jsonSubOrderObj)

        jsonOrderObj['subOrder'] = jsonSubOrderList

    return HttpResponse(json.dumps({'order': jsonOrderObj}), content_type='application/json')


def modifyOrder(request):
    oid = request.POST['oid']
    buyer = request.POST['detailBuyer']
    order_date_str = request.POST['detailOrderDate']
    due_date_str = request.POST['detailDueDate']
    print(due_date_str)
    order_type = request.POST['detailOrderType']
    order_inout = request.POST['detailOrderInout']
    order_round = request.POST['detailRound']
    sub_order_code = int(request.POST['subOrderCode'])
    sub_design_qty = int(request.POST['subDesignQty'])


    order = Order.objects.get(id=oid)

    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

    order_date = datetime.strptime(order_date_str, '%Y-%m-%d').date()
    order.buyer = buyer
    order.order_Date = order_date
    order.due_date = due_date
    order.order_type = order_type
    order.order_inout = order_inout
    order.order_round = order_round

    order.save()

    designOrder = Order_DesignData.objects.get(order_id=order, code=str(order.code)+'-'+str(sub_order_code+1))
    designOrder.design_qty = sub_design_qty
    designOrder.save()

    return redirect('/order')

@csrf_exempt
def delete(request):
    oid = request.POST['orderId']
    order = Order.objects.get(id=oid)

    order.delete()

    return redirect('/order')
def warpTable(request, id):
    tablebot = []
    try:
        warptopJSON = requests.get("http://tnswebserver.iptime.org:1978/api/tws_chart").json()#1번
        warpbotJSON = requests.get("http://tnswebserver.iptime.org:1978/api/tws_chart/beam").json()#2번
        for jsontop in warptopJSON['tws_chart_']:
            if jsontop['tws_order_make_number'] == '56':
                warpTabletop = {}
                warpTabletop['yarn_name'] = jsontop["tws_order_yarn_name"]
                warpTabletop['setno'] = jsontop['tws_order_set_number']
                warpTabletop['lotno'] = jsontop['tws_order_lot_number']
                warpTabletop['bon_number'] = jsontop['tws_order_machine_nmuber']
                warpTabletop['bim_number'] = jsontop['tws_order_bm_number']
                warpTabletop['creel_speed'] = jsontop['tws_order_creel_speed']
                warpTabletop['warper_speed'] = jsontop['tws_order_warper_speed']
                warpTabletop['drift'] = jsontop['tws_order_pre_stretch']
                warpTabletop['tention'] = jsontop['tws_order_final_stretch']
        for jsonbot in warpbotJSON['warper_beam_']:
            if jsonbot['tws_order_make_number'] == '52':
                warpTablebot = {}
                warpTablebot['beam_no'] = jsonbot['warperbeam_code']
                warpTablebot['meter'] = jsonbot['tws_warper_total_length']
                warpTablebot['turn_count'] = jsonbot['tws_current_turncnt']
                warpTablebot['warp_time1'] = jsonbot['tws_time1']
                warpTablebot['warp_time2'] = jsonbot['tws_time2']
                warpTablebot['beam_circum'] = jsonbot['tws_warper_outside']
                warpTablebot['warp_manage'] = jsonbot['user_name']
                tablebot.append(warpTablebot)
    except Exception as e:
        print(e)
    variables = {'top': warpTabletop, 'bot': tablebot, 'userlang':request.user}
    return render(request, 'worksheet/warp.html', variables)


@csrf_exempt
def rawroll(request, id):
    if request.method == "GET":
        order = Order.objects.get(id=id)
        buyer = order.buyer
        order_sub = Order_DesignData.objects.get(order_id=id)
        company = Company.objects.get(id=1)
        #design_name = FSTY_CAD_Design_Data.objects.get(id=order_sub.de)

        account = Account.objects.get(accountname=buyer)
        return render(request, 'worksheet/rawroll.html', {'orderaccount':account,'order_sub':order_sub,'order':order, 'company':company})

class Order_design_data_api(viewsets.ModelViewSet):
    queryset = Order_DesignData.objects.all()
    serializer_class = Order_design_Serializer

class Order_api(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('pk')
    serializer_class = Order_Serializer

class Order_end_api(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = Order_Serializer


@csrf_exempt
def getstyleByJson(request, orderId):
    style_order = Style_orders.objects.get(pk=orderId)
    jsonStyleObj = {}
    jsonStyleObj['FabricVersion'] = style_order.style_ver
    jsonStyleObj['FabricCode'] = style_order.fabric_info.fabric_code
    jsonStyleObj['FabricName'] = style_order.fabric_info.fabric_name
    jsonStyleObj['FabricSize'] = style_order.fabric_info.fabric_size
    jsonStyleObj['SMeterWeight'] = style_order.fabric_info.sMeter_width
    jsonStyleObj['YardWeight'] = style_order.fabric_info.yard_weight
    jsonStyleObj['FabricPart'] = style_order.fabric_info.fabric_part
    jsonStyleObj['FabricLoss'] = style_order.fabric_info.FabricLoss
    jsonStyleObj['FabricCsm'] = style_order.fabric_info.FabricCsm
    jsonStyleObj['FabricConstruction'] = style_order.fabric_info.fabric_Construction
    jsonStyleObj['FabricWidth'] = style_order.fabric_info.fabric_width
    jsonStyleObj['CuttableWidth'] = style_order.fabric_info.cuttable_width
    jsonStyleObj['Unit'] = style_order.fabric_info.unit
    jsonStyleObj['DyeProcessTypeCode'] = style_order.fabric_info.dyeProcessTypeCode
    jsonStyleObj['oid'] = style_order.pk
    try:
        jsonStyleObj['YarnCode'] = style_order.fabric_info.yarn.st_yarn_code
        jsonStyleObj['YarnName'] = style_order.fabric_info.yarn.st_yarn_name
        jsonStyleObj['YarnColor'] = style_order.fabric_info.yarn.st_yarn_color
        jsonStyleObj['ContentRate'] = style_order.fabric_info.yarn.st_yarn_rate
        jsonStyleObj['YarnCount'] = style_order.fabric_info.yarn.st_yarn_cnt
        jsonStyleObj['YnDye'] = style_order.fabric_info.yarn.yn_Dye
    except Exception as e:
        print(e)
        jsonStyleObj['YarnCode'] = ''
        jsonStyleObj['YarnName'] = ''
        jsonStyleObj['YarnColor'] = ''
        jsonStyleObj['ContentRate'] = ''
        jsonStyleObj['YarnCount'] = ''
        jsonStyleObj['YnDye'] = ''

    return HttpResponse(json.dumps(jsonStyleObj), content_type='application/json')

@csrf_exempt
def Style_modify(request, orderId):
    print("리퀘스트", request)
    style_order = Style_orders.objects.get(pk=orderId)
    jsonObj = {}
    test = []
    # try:
    print("1")
    # if style_order.fabric_info.yarn.yn_Dye == False:
    #     yn_Dye = False
    try:
        if style_order.fabric_info.yarn.yn_Dye == True:
            ynd = True.__str__()
            yn_Dye = "true"
            print("yn_Dye",ynd)
        else:
            ynd = False.__str__()
            yn_Dye = "false"
            print("yn_Dye", ynd)
        data = [{
            'StyleKey': style_order.style_key,
            'Fabrics': [{
                'FabricVersion': int(style_order.style_ver),
                'FabricCode': style_order.fabric_info.fabric_code,
                'FabricName': str(request.POST['FabricName']),
                # 'FabricName': 'test',
                'FabricColor': style_order.fabric_info.fabric_color,
                'FabricSize': request.POST['FabricSize'],
                'FabricPart': request.POST['FabricPart'],
                'FabricConstruction': request.POST['FabricConstruction'],
                'FabricWidth': float(request.POST['FabricWidth']),
                'CuttableWidth': float(request.POST['CuttableWidth']),
                'SMeterWeight': float(request.POST['SMeterWeight']),
                'YardWeight': float(request.POST['YardWeight']),
                'Unit': request.POST['Unit'],
                'FabricLoss': float(request.POST['FabricLoss']),
                'FabricCsm': float(request.POST['FabricCsm']),
                'DyeProcessTypeCode': style_order.fabric_info.dyeProcessTypeCode,
                'DyeCompanyCode': style_order.fabric_info.dyeCompanyCode,
                'KnitCompanyCode': style_order.fabric_info.knitCompanyCode,
                'Yarns': [{
                    'YarnCode': style_order.fabric_info.yarn.st_yarn_code,
                    'YarnName': request.POST['YarnName'],
                    # 'YarnName': 'testyarn',
                    'YarnColor': style_order.fabric_info.yarn.st_yarn_color,
                    'ContentRate': float(request.POST['ContentRate']),
                    'YarnCount': int(style_order.fabric_info.yarn.st_yarn_cnt),
                    'YnDye': yn_Dye
                }]
            }]
        }]
        jsonObj['Key'] = style_order.style_key
        jsonObj['Content'] = data.__str__()
    except Exception as e:
        print("error: ", e)
    print("2")
    # except:
    #     if style_order.fabric_info.yarn.yn_Dye == True:
    #         yn_Dye = True
    #     jsonObj['StyleKey'] = style_order.style_key
    #     jsonObj['Fabrics'] = [{
    #                 'FabricVersion': int(style_order.style_ver),
    #                 'FabricCode': style_order.fabric_info.fabric_code,
    #                 # 'FabricName': str(request.POST['FabricName']),
    #                 'FabricName': 'test',
    #                 'FabricColor': style_order.fabric_info.fabric_color,
    #                 'FabricSize': request.POST['FabricSize'],
    #                 'FabricPart': request.POST['FabricPart'],
    #                 'FabricConstruction': request.POST['FabricConstruction'],
    #                 'FabricWidth': float(request.POST['FabricWidth']),
    #                 'CuttableWidth': float(request.POST['CuttableWidth']),
    #                 'SMeterWeight': float(request.POST['SMeterWeight']),
    #                 'YardWeight': float(request.POST['YardWeight']),
    #                 'Unit': request.POST['Unit'],
    #                 'FabricLoss': float(request.POST['FabricLoss']),
    #                 'FabricCsm': float(request.POST['FabricCsm']),
    #                 'DyeProcessTypeCode': style_order.fabric_info.dyeProcessTypeCode,
    #                 'DyeCompanyCode': style_order.fabric_info.dyeCompanyCode,
    #                 'KnitCompanyCode': style_order.fabric_info.knitCompanyCode,
    #                 'Yarns': [{
    #                     'YarnCode': style_order.fabric_info.yarn.st_yarn_code,
    #                     # 'YarnName': request.POST['YarnName'],
    #                     'YarnName': 'testyarn',
    #                     'YarnColor': style_order.fabric_info.yarn.st_yarn_color,
    #                     'ContentRate': float(request.POST['ContentRate']),
    #                     'YarnCount': int(style_order.fabric_info.yarn.st_yarn_cnt),
    #                     # 'YnDye': style_order.fabric_info.yarn.yn_Dye,  # 값소문자
    #                     'YnDye': yn_Dye
    #                 }]
    #     }]
    #     data = {
    #         "StyleKey": style_order.style_key,
    #         "Fabrics": [
    #             {
    #                 "FabricVersion": int(style_order.style_ver),
    #                 "FabricCode": style_order.fabric_info.fabric_code,
    #                 "FabricName": 'test',
    #                 # "FabricName": request.POST['FabricName'],
    #                 "FabricColor": style_order.fabric_info.fabric_color,
    #                 "FabricSize": request.POST['FabricSize'],
    #                 "FabricPart": request.POST['FabricPart'],
    #                 "FabricConstruction": request.POST['FabricConstruction'],
    #                 "FabricWidth": float(request.POST['FabricWidth']),
    #                 "CuttableWidth": float(request.POST['CuttableWidth']),
    #                 "SMeterWeight": float(request.POST['SMeterWeight']),
    #                 "YardWeight": float(request.POST['YardWeight']),
    #                 "Unit": request.POST['Unit'],
    #                 "FabricLoss": float(request.POST['FabricLoss']),
    #                 "FabricCsm": float(request.POST['FabricCsm']),
    #                 "DyeProcessTypeCode": style_order.fabric_info.dyeProcessTypeCode,
    #                 "DyeCompanyCode": style_order.fabric_info.dyeCompanyCode,
    #                 "KnitCompanyCode": style_order.fabric_info.knitCompanyCode,
    #                 "Yarns": [
    #                     {
    #                         "YarnCode": style_order.fabric_info.yarn.st_yarn_code,
    #                         "YarnName": 'testyarnname',
    #                         # "YarnName": request.POST['YarnName'],
    #                         "YarnColor": style_order.fabric_info.yarn.st_yarn_color,
    #                         "ContentRate": float(request.POST['ContentRate']),
    #                         "YarnCount": int(style_order.fabric_info.yarn.st_yarn_cnt),
    #                         "YnDye": style_order.fabric_info.yarn.yn_Dye
    #                     }
    #                 ]
    #             }
    #         ],
    #     }
    # except:
    #     data = {
    #         "StyleKey":style_order.style_key,
    #         "Fabrics":[
    #             {
    #                 "FabricVersion": int(style_order.style_ver),
    #                 "FabricCode": style_order.fabric_info.fabric_code,
    #                 "FabricName": 'test',
    #                 # "FabricName": request.POST['FabricName'],
    #                 "FabricColor": style_order.fabric_info.fabric_color,
    #                 "FabricSize": request.POST['FabricSize'],
    #                 "FabricPart": request.POST['FabricPart'],
    #                 "FabricConstruction": request.POST['FabricConstruction'],
    #                 "FabricWidth": float(request.POST['FabricWidth']),
    #                 "CuttableWidth": float(request.POST['CuttableWidth']),
    #                 "SMeterWeight": float(request.POST['SMeterWeight']),
    #                 "YardWeight": float(request.POST['YardWeight']),
    #                 "Unit": request.POST['Unit'],
    #                 "FabricLoss": float(request.POST['FabricLoss']),
    #                 "FabricCsm": float(request.POST['FabricCsm']),
    #                 "DyeProcessTypeCode": style_order.fabric_info.dyeProcessTypeCode,
    #                 "DyeCompanyCode": style_order.fabric_info.dyeCompanyCode,
    #                 "KnitCompanyCode": style_order.fabric_info.knitCompanyCode,
    #                 "Yarns": [
    #                     {
    #                         "YarnCode": style_order.fabric_info.yarn.st_yarn_code,
    #                         "YarnName": 'testyarnname',
    #                         # "YarnName": request.POST['YarnName'],
    #                         "YarnColor": style_order.fabric_info.yarn.st_yarn_color,
    #                         "ContentRate": float(request.POST['ContentRate']),
    #                         "YarnCount": int(style_order.fabric_info.yarn.st_yarn_cnt),
    #                         "YnDye": style_order.fabric_info.yarn.yn_Dye
    #                     }
    #                 ]
    #             }
    #         ],
    #     }
    print("3")
    content = json.dumps(jsonObj)
    print("스타일 개발의뢰 원단 정보 변경", content)
    # headers = {
    #     'Content-Type': "application/json",
    #     # 'Content-Type': 'multipart/form-data; charset=UTF-8' % content,
    #     # 'Content-Type': 'multipart/form-data; '
    #     #                 'boundary=%s'%content,
    #     'ApiKey': '4eeca0624bd04dbba644963e2819b89c',
    # }
    try:
        headers = {
            'Content-Type': "application/json",
            'ApiKey': '4eeca0624bd04dbba644963e2819b89c',
        }
        # 스타일 개발의뢰 원단 정보 변경
        style_ck = requests.post('http://api.lookiss.com:9403/api/SCC/UpdateStyleFabricByForm', headers=headers,
                                 data=content)
        print("스타일 개발의뢰 원단 정보 변경 :", style_ck.status_code)

        # 스타일 의뢰 리스트 리쿼스트 data확인

        if style_ck.status_code == 200:
            respose = json.loads(style_ck.text)
            print("리스폰스", respose)
            style_ordersave = Style_orders.objects.get(pk=orderId)
            style_ordersave.style_ver = int(style_ordersave.style_ver)+1
            style_ordersave.save()
    except:
        pass
    return HttpResponse(json.dumps(jsonObj), content_type='application/json')

@csrf_exempt
def Style_suc(request, orderId):
    style_order = Style_orders.objects.get(pk=orderId)
    jsonobj = {}
    jsonobj['StyleKey'] = style_order.style_key
    jsonobj['Status'] = 'COMPLETED'
    content = json.dumps(jsonobj)
    headers = {
        'Content-Type': "application/json",
        'ApiKey': '4eeca0624bd04dbba644963e2819b89c',
    }
    #스타일 개발의뢰 상태 변경완료
    print("content : ", content)
    style_ck = requests.post('http://api.lookiss.com:9403/api/SCC/ChangeStyleStatus', headers=headers, data=content)
    print("스타일 개발의뢰 상태 변경 :", style_ck.status_code)
    # style_ckJSON = requests.get("http://api.lookiss.com:9403/api/SCC/ChangeStyleStatus").json()  # 1번
    # print("스타일 개발의뢰 상태 변경 메세지", style_ckJSON)
    return HttpResponse(json.dumps(jsonobj), content_type='application/json')


@csrf_exempt
def order_end(request):
    print("request: ",request)
    try:
        today = datetime.today()
        today = datetime.strftime(today,'%Y-%m-%d')
        todayuq = datetime.strftime(today,'%Y-%m-%d,%H:%M:%S')
        oid = request.POST['oid']
        print("oid?",oid)
        #추후에 roll 들어오면 쓸예정
        roll_count = request.POST['roll_count']
        print("roll_count",roll_count)
        order = Order.objects.get(pk=oid)
        order.state = 2
        print("order :", order.code)
        order.save()
        order_design = Order_DesignData.objects.get(order_id=oid)
        style_odr = Style_orders.objects.get(style_key=order.code)
        print("style_odr stylekey : ", style_odr.style_key)
        print("style_odr : ", style_odr.fabric_info.fabric_code)
        print("style_odr fabric_info : ", style_odr.fabric_info)
        # order_style_fb = Style_fabric.objects.get(fabric_code=style_odr.fabric_info.fabric_code)
        # name = order_style_fb.fabric_name
        name = style_odr.fabric_info.fabric_name
        print("name: ", name)
        qty = order_design.design_qty
        print("qty :", qty)
        raw = Raw.objects.create(item_name=name, designData_id=order_design.design_data_id, qty=qty, input_date=today,
                                 request_com=order.company)
        print("raw: ", raw)
        raw.save()
        # print("stlye fabric matching ck: ", order_design.design_data_id.CAD_Design_Data_code)
        # print("stlye fabric name :", name)
        # ordersf = Style_fabric.objects.get(fabric_name=name)
        # print("order_style_fb :", order_style_fb)
        # print("order_style_fb : ", order_style_fb.value)
        if order.value == True:
            print("order.buyer",order.buyer)
            buyer = Account.objects.get(id=order.buyer)
            if buyer.accountmanager == 'None':
                buyer_manager = ''
            else:
                buyer_manager = buyer.accountmanager
            company = Company.objects.get(id=1)
            jsonObj = {}
            data = [{
                'KnitOutKey': todayuq,#order_design.qr_code,
                'KnitWorkKey': order.knitWorkKey,
                'OutDate': today,
                'SupplierCode': style_odr.fabric_info.knitCompanyCode,
                'SupplierName': style_odr.fabric_info.knitCompanyName,
                'CustomerCode': style_odr.fabric_info.dyeCompanyCode,
                'CustomerName': buyer_manager,
                'CustomerUser': buyer.accountname,
                'CustomerTel': buyer.accountnum,
                'CustomerAddress': buyer.accountaddress,
                'RollCount': roll_count,  # raw.pk
                'Remark': '',
                'Items': [{
                    'StyleKey': order.code,
                    'FabricCode': style_odr.fabric_info.fabric_code,
                    'FabricName': style_odr.fabric_info.fabric_name,
                    'FabricColor': style_odr.fabric_info.fabric_color,
                    'FabricSize': style_odr.fabric_info.fabric_size,
                    'Unit': style_odr.fabric_info.unit,  # Yds,
                    'RollNo': raw.pk,
                    'OutQty': int(raw.qty),
                }]
            }]
            jsonObj['Key'] = style_odr.style_key
            jsonObj['Content'] = data.__str__()

            #######################################################################################
            # if order.value == True:
            #     print("order.buyer", order.buyer)
            #     buyer = Account.objects.get(id=order.buyer)
            #     jsonObj = {}
            #     jsonObj['KnitOutKey'] = style_odr.fabric_info.dyeCompanyCode
            #     jsonObj['KnitWorkKey'] = order.knitWorkKey
            #     jsonObj['OutDate'] = today
            #     jsonObj['SupplierCode'] = order.manager.pk
            #     jsonObj['SupplierName'] = order.company
            #     jsonObj['CustomerCode'] = buyer.pk
            #     jsonObj['CustomerName'] = buyer.accountmanager
            #     jsonObj['CustomerUser'] = buyer.accountname
            #     jsonObj['CustomerTel'] = ''
            #     jsonObj['CustomerAddress'] = buyer.accountaddress
            #     jsonObj['RollCount'] = roll_count  # raw.pk
            #     jsonObj['Remark'] = ''
            #     jsonObj['Items'] = [{
            #         'StyleKey': order.code,
            #         'FabricCode': order_design.design_data_id.CAD_Design_Data_code,
            #         'FabricName': order_design.design_data_id.CAD_Design_Data_name,
            #         'FabricColor': style_odr.fabric_info.fabric_color,
            #         'FabricSize': style_odr.fabric_info.fabric_size,
            #         'Unit': style_odr.fabric_info.unit,  # Yds,
            #         'RollNo': raw.pk,
            #         'OutQty': int(raw.qty),
            #     }]
            print("json obj", jsonObj.values())
            content = json.dumps(jsonObj)
            # content = bytes(json.dumps(jsonObj), encoding='utf-8')
            print("content : ", content)
            headers = {
                'Content-Type': "application/json; charset=UTF-8",
                # 'Content-Type': 'multipart/form-data' % content,
                'ApiKey': '4eeca0624bd04dbba644963e2819b89c',
            }

            style_ck = requests.post('http://api.lookiss.com:9403/api/SCC/RegistKnitFabricOutByForm', headers=headers,
                                     data=content)

            print("스타일체크", style_ck.status_code)
            # respose = json.loads(style_ck.text)
            # print("리스폰스", respose)
        context = {'msg': 'suc'}
    except Exception as e:
        print("error리스폰스 : ", e)
        context = {'msg': 'False'}
    print("htmlres : ", HttpResponse(json.dumps(context), content_type='application/json;charset=utf-8'))
    return HttpResponse(json.dumps(context), content_type='application/json')
