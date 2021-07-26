import json, datetime

from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from machine.models import Warp_Machine, Knit_Machine
from order.models import *
from materials.models import *
from schedule.models import Warp_Process, Knit_Process


@login_required(login_url='/')
@csrf_exempt
def showMaterial(request):
    orderList = Order.objects.all()
    yarnList = Yarn.objects.all()
    for yarnObj in yarnList:
        yarnObj.lab = RGBtoLAB(yarnObj.color)
    beamList = Beam.objects.all()
    rollList = Roll.objects.all()
    raw = Raw.objects.all()

    return render(request, 'material.html', {'title': 'Materials', 'yarnList': yarnList, 'beamList': beamList, 'orderList':orderList, 'rollList':rollList, 'userlang':request.user, 'raw':raw})

def RGBtoLAB(hexCode):

    R = int(hexCode[1:3], 16)
    G = int(hexCode[3:5], 16)
    B = int(hexCode[5:7], 16)

    var_R = float(R) / 255
    var_G = float(G) / 255
    var_B = float(B) / 255

    if var_R > 0.03928:
        var_R = pow(( var_R + 0.055 ) / 1.055 , 2.4)
    else:
        var_R = var_R / 12.92

    if var_G > 0.03928:
        var_G = pow(( var_G + 0.055 ) / 1.055 , 2.4)
    else:
        var_G = var_G / 12.92

    if var_B > 0.03928:
        var_B = pow(( var_B + 0.055 ) / 1.055 , 2.4)
    else:
        var_B = var_B / 12.92

    var_R = var_R * 100
    var_G = var_G * 100
    var_B = var_B * 100

    var_X_D65 = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    var_Y_D65 = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    var_Z_D65 = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

    if 1:
        var_X_D65 = var_X_D65 * 1.0479 + var_Y_D65 * 0.0229 + var_Z_D65 * -0.0502
        var_Y_D65 = var_X_D65 * 0.0296 + var_Y_D65 * 0.9904 + var_Z_D65 * -0.0171
        var_Z_D65 = var_X_D65 *-0.0092 + var_Y_D65 * 0.0151 + var_Z_D65 * 0.7519

    if 1:
        var_X = var_X_D65 /  96.43
        var_Y = var_Y_D65 / 100.00
        var_Z = var_Z_D65 /  82.51
    elif 0:
        var_X = var_X_D65 /  95.047
        var_Y = var_Y_D65 / 100.000
        var_Z = var_Z_D65 / 108.883

    if var_X > 0.008856:
        var_X = pow(var_X, 1.0/3)
    else:
        var_X = ( 7.787 * var_X ) + ( 16.0 / 116 )

    if var_Y > 0.008856:
        var_Y = pow(var_Y, 1.0/3)
    else:
        var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116 )

    if var_Z > 0.008856:
        var_Z = pow(var_Z, 1.0/3)
    else:
        var_Z = ( 7.787 * var_Z ) + ( 16.0 / 116 )


    L_str = str(round(( 116 * var_Y ) - 16))
    A_str = str(round(500 * ( var_X - var_Y )))
    B_str = str(round(200 * ( var_Y - var_Z )))

    return L_str+"/"+A_str+"/"+B_str


@csrf_exempt
def searchYarn(request):
    searchName = request.POST['searchName']

    yarnDictList = []

    yarnList = Yarn.objects.filter(name__contains=searchName).values()
    for yarnObj in yarnList:
        yarnObj['lab'] = RGBtoLAB(yarnObj['color'])
        yarnDictList.append(yarnObj)

    return HttpResponse(json.dumps(yarnDictList), content_type='application/json')

@csrf_exempt
def searchBeam(request):
    searchName = request.POST['searchName']

    beamDictList = []

    beamList = Beam.objects.filter(name__contains=searchName).values()

    for beamObj in beamList:

        if beamObj['yarn_id'] != None:
            beamObj['yarn_name'] = Yarn.objects.get(pk=beamObj['yarn_id']).name
        else:
            beamObj['yarn_name'] = ''
        beamDictList.append(beamObj)

    return HttpResponse(json.dumps(beamDictList), content_type='application/json')

def createYarn(request):

    name = request.POST['yarnName']
    code = request.POST['yarnCode']
    maker = request.POST['yarnMaker']
    count = request.POST['yarnCount']
    filament = request.POST['yarnFilament']
    contraction = request.POST['yarnContraction']
    material = request.POST['yarnMaterial']
    kind = request.POST['yarnKind']
    color = request.POST['yarnColor']
    weight = request.POST['yarnWeight']
    qty = request.POST['yarnQty']


    yarn = Yarn(name=name, code=code, maker=maker, count=count, filament=filament, contraction=contraction, material=material, kind=kind, color=color, weight=weight ,qty=qty)
    yarn.save()

    return redirect('/material')

def createBeam(request):
    name = request.POST['beamName']
    size = request.POST['beamSize']

    beam = Beam(name = name, size = size)
    beam.save()

    return redirect('/material')

def createRoll(request):

    rollname = request.POST['rollname']
    rollfabricname = request.POST['rollfabricname']
    rollfabricdate = request.POST['rollfabricdate']
    rolloutdate = request.POST['rolloutdate']
    rollcount = request.POST['rollcount']
    rollfabricerror = int(request.POST['rollfabricerror'])
    rollfabriclength = int(request.POST['rollfabriclength'])
    rollfabricweight = request.POST['rollfabricweight']
    rollfabrictrue = rollfabriclength - rollfabricerror

    roll = Roll(rollname=rollname, rollfabricname=rollfabricname,rollfabricdate=rollfabricdate, rolloutdate=rolloutdate, rollcount=rollcount, rollfabricerror=rollfabricerror, rollfabriclength=rollfabriclength,rollfabrictrue=rollfabrictrue,rollfabricweight=rollfabricweight )

    roll.save()

    return redirect('/material')

@csrf_exempt
def getYarnInfoByJson(request):
    id = request.POST['id']

    yarn = model_to_dict(Yarn.objects.get(pk=id))

    return HttpResponse(json.dumps(yarn), content_type='application/json')

@csrf_exempt
def beamDelete(request):
    bid = request.POST['bid']
    try:
        delBeam = Beam.objects.get(id=bid)
        delBeam.delete()

        return HttpResponse(json.dumps({'success':True}), content_type='application/json')

    except:

        return HttpResponse(json.dumps({'success': False}), content_type='application/json')

@csrf_exempt
def greigeDelete(request):
    gpk = request.POST['gpk']
    try:
        delGreige = Raw.objects.get(id=gpk)
        delGreige.delete()

        return HttpResponse(json.dumps({'success':True}), content_type='application/json')

    except:

        return HttpResponse(json.dumps({'success': False}), content_type='application/json')



@csrf_exempt
def yarnDelete(request):
    id = request.POST['id']
    try:
        delYarn = Yarn.objects.get(id=id)
        delYarn.delete()

        return HttpResponse(json.dumps({'success':True}), content_type='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


@csrf_exempt
def createRaw(request):
    if request.method == 'POST':
        print(request)
        order_id = request.POST['order_id']
        machine_id = request.POST['machine_id']
        print(order_id)
        print(machine_id)
        context = {'success':True}
        return HttpResponse(json.dumps(context), content_type='application/json')
        #today = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        #knit_mc = Knit_Machine.objects.get(tns_code=machine_id).id
        #order_process = Knit_Process.objects.get(knit_machine_id=knit_mc)
        #order_process.real_end_time = today
        #order = Order_DesignData.objects.get(code=order_id)
        #order_set = Order.objects.get(code=order_id)
        #order_set.cheack = True
        #raw_create = Raw.objects.create(qty=order.design_qty, designData_id=order.design_data_id, item_name=order.design_data_id.CAD_Design_Data_name, input_date=today)
        #order_set.save()
        #raw_create.save()
        #order_process.save()
        # api 데이터 넘기는 소