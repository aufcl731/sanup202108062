import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from account.models import Company
from design_data.models import *
from order.models import Order, Order_DesignData
import datetime
from django.utils import timezone


# order 등록수정해야 할점 시간이 무조건 15:00 로 들어감. html order_date 를 disabled 하고 현재시간으로 세팅하는게 바람직해보임.

@login_required(login_url='/')
def order(request):
    title = 'Order'
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
        # 하지만, order_date 는 위에 쓴 것처럼 현재 시간으로 설정하는게 좋을거같음.
        #order_date = datetime.datetime.strptime(order_date_str, '%Y-%m-%d').date()

        due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
        order_date = timezone.localtime()


        #Updated upstream
        # 오더코드 = 현재시간 + 오더타입 + 오더인아웃
        order_code = datetime.datetime.today().strftime("%Y%m%d%H%M%S")[2:] + str(order_type) + str(order_inout)
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

    orderList = Order.objects.all().order_by('id')
    designList = FSTY_CAD_Design_Data.objects.all().order_by("-CAD_Design_Data_id")


    return render(request, 'order.html', {'title':title, 'designCount':designList.count(), 'orderCount':orderList.count(), 'designDataList': designList, 'orderList': orderList, 'company': myCompany.name})


'''@csrf_exempt
def getOrderByJson(request):
    jsonOrder = []
    orderList = Order.objects.
'''
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
    return HttpResponse(json.dumps({}), content_type='application.json')
@csrf_exempt
def showQr(request, id):
    print(id)
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
    order_type = request.POST['detailOrderType']
    order_inout = request.POST['detailOrderInout']
    order_round = request.POST['detailRound']
    sub_order_code = int(request.POST['subOrderCode'])
    sub_design_qty = int(request.POST['subDesignQty'])


    order = Order.objects.get(id=oid)

    due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()

    order_date = datetime.datetime.strptime(order_date_str, '%Y-%m-%d').date()
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

def warpTable(request):


    return render(request, 'worksheet/warp.html', {})


def rawroll(request):

    return render(request, 'worksheet/rawroll.html', {})