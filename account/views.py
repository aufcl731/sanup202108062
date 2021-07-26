#-*- coding:utf-8 -*-

import json
import datetime
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from account.forms import UserForm, LoginForm
from account.models import User, Company
from machine.models import Warp_Machine, Knit_Machine
from order.models import Order, Order_DesignData

#tns test용
@csrf_exempt
def pjs1234(request):
    username = request.POST['username']
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    create_date = request.POST['create_date']
    theme_code = request.POST['theme_code']
    lang_code = request.POST['lang_code']

    sendUser = {'username':username, 'name':name, 'email':email, 'phone':phone, 'create_date':create_date, 'theme_code':theme_code, 'lang_code':lang_code}

    return HttpResponse(json.dumps(sendUser), content_type='application/json')

def signUo(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                company = Company.objects.get(id=1)
                level = 1
                User.objects.create_user(username=user.username, email=user.email, phone=user.phone, password=user.password, level=level , name=user.name, is_active=False, company_code=company)
                return redirect('/')
        else:
            form = UserForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('/')
def userratingset(request, id):

    return render(request, 'order.html')
def login_site(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            try:
                user_active = User.objects.get(username=username)

            except Exception:
                msg = '아이디, 비밀번호를 확인해주세요'
                return render(request, 'msg/errorPage.html', {'msg': msg})

            if user_active.is_active:
                user = authenticate(username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('/server')
                else:
                    msg = '아이디, 비밀번호를 확인해주세요'
                    return render(request, 'msg/errorPage.html', {'msg': msg})
            else:
                msg = '승인대기중입니다.'
                return render(request, 'msg/errorPage.html', {'msg': msg})
        else:
            form = LoginForm()
            return render(request, 'login.html', {'form': form})
    else:
        return redirect('/dashboard')

@login_required(login_url='/')
def dashboard(request):
    orderList = Order.objects.all()
    totalOrder = Order.objects.all().count()
    pendingOrder = Order.objects.filter(state=0).count()
    progressOrder = Order.objects.filter(state=1).count()
    compOrder = Order.objects.filter(state=2).count()
    knit_machine = Knit_Machine.objects.all()

    #warp_Machine = Warp_Machine.objects.all().count()
    #on_warp_Machine = Warp_Machine.objects.filter(tws_onoff='on').count()

    #knit_Machine = Knit_Machine.objects.all().count()
    #on_knit_Machine = Knit_Machine.objects.filter(trs_onoff='on').count()

    #all_machine_count = warp_Machine + knit_Machine
    #on_machine_count = on_warp_Machine + on_knit_Machine

    designOrderList = Order_DesignData.objects.all().order_by('-id')[:13]

    user = request.user

    x = str(user.company_code.x)
    y = str(user.company_code.y)

    weatherList = []
    try:
        knitJsonData = requests.get("http://tnswebserver.iptime.org:1978/api/trs").json()
        warpJsonData = requests.get("http://tnswebserver.iptime.org:1978/api/tws").json()
        weatherXml = requests.get('http://www.kma.go.kr/wid/queryDFS.jsp?gridx=' + x + '&gridy=' + y)

        totalplaytime = 0
        ttrsmachineplaytime = 0
        ttwsmachineplaytime = 0
        for trsplay in knitJsonData['trs']:
            if trsplay['date_to_time'] != None:
                trsmachineplaytime = trsplay['date_to_time']
                ttrsmachineplaytime = ttrsmachineplaytime + trsmachineplaytime
        for twsplay in warpJsonData['tws']:
            if twsplay['date_to_time'] != None:
                twsmachineplaytime = twsplay['date_to_time']
                ttwsmachineplaytime = ttwsmachineplaytime + twsmachineplaytime

        totalplaytime = ttrsmachineplaytime + ttwsmachineplaytime
        root = ET.fromstring(weatherXml.text).find('body')
        totaltime = 0
        trstotaltime = 0
        twstotaltime = 0
        for weatherObj in root.findall('data'):
            weatherDict = {}
            weatherDict['hour'] = weatherObj.find('hour').text
            weatherDict['reh'] = weatherObj.find('reh').text
            weatherDict['wfEn'] = weatherObj.find('wfEn').text
            weatherDict['pop'] = weatherObj.find('pop').text
            weatherDict['temp'] = int(float(weatherObj.find('temp').text))
            weatherList.append(weatherDict)

        ts = int(ET.fromstring(weatherXml.text).find('header').find('ts').text)

        all_knit_machine = len(knitJsonData["trs"])
        all_warp_machine = len(warpJsonData["tws"])
        on_knit_machine = 0
        on_warp_machine = 0

        # 경편기 및 정경기 보유기간

        for knittime in knitJsonData['trs']:
            if knittime['trs_installation_time'] != '':
                nowtimech = str(datetime.datetime.today().strftime("%y-%m-%d %H:%M:%S"))
                nowtimecount = datetime.datetime.strptime(nowtimech, "%y-%m-%d %H:%M:%S")
                stringtime = knittime['trs_installation_time']
                machinetime = datetime.datetime.strptime(stringtime, "%Y-%m-%d %H:%M:%S")
                totalminetime = (nowtimecount - machinetime).days * 24
                trstotaltime = trstotaltime + totalminetime

        for warptime in warpJsonData['tws']:
            if warptime['tws_installation_time'] != '':
                twsnowtimech = str(datetime.datetime.today().strftime("%y-%m-%d %H:%M:%S"))
                twsnowtimecount = datetime.datetime.strptime(twsnowtimech, "%y-%m-%d %H:%M:%S")
                twsstringtime = warptime['tws_installation_time']
                twsmachinetime = datetime.datetime.strptime(twsstringtime, "%Y-%m-%d %H:%M:%S")
                twstotalminetime = (twsnowtimecount - twsmachinetime).days *24
                twstotaltime = twstotaltime + twstotalminetime

        totaltime = twstotaltime + trstotaltime

        # 경편기 On 카운트
        for knitOn in knitJsonData["trs"]:
            if knitOn["trs_onoff"] == "ON":
                on_knit_machine = on_knit_machine + 1

        # 정경기 On 카운트
        for warpOn in warpJsonData["tws"]:
            if warpOn["tws_onoff"] == "ON":
                on_warp_machine = on_warp_machine + 1

        all_machine_count = all_knit_machine + all_warp_machine
        on_machine_count = on_knit_machine + on_warp_machine

    except Exception as e:

        print(e)
        all_machine_count = 0
        on_machine_count = 0


    title = 'Dashboard'

    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)

    variables = {'title':title, 'totalOrder':totalOrder, 'pendingOrder':pendingOrder, 'progressOrder':progressOrder,
                 'compOrder': compOrder, 'designOrderList': designOrderList,'all_machine_count':all_machine_count,
                 'on_machine_count':on_machine_count, 'weatherList': weatherList, 'now': now, 'tomorrow': tomorrow,
                 'orderList': orderList, 'ts': ts, 'totaltime': totaltime , 'totalplaytime': totalplaytime, 'userlang':request.user}

    return render(request, 'index.html', variables)

def logout_site(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def server(request):
    return render(request, 'server.html', {})
