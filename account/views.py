import datetime
import json

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

def aaaa(request):
    return render(request, 'schedule20191101.html')

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

    print(sendUser)
    return HttpResponse(json.dumps(sendUser), content_type='application/json')

def signUo(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                company = Company.objects.get(id=1)
                User.objects.create_user(username=user.username, email=user.email, phone=user.phone, password=user.password, name=user.name, is_active=False, company_code=company)
                return redirect('/')
        else:
            form = UserForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('/')

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
        knitJsonData = requests.get("http://tnswebserver.iptime.org:1978/values/trs").json()
        warpJsonData = requests.get("http://tnswebserver.iptime.org:1978/values/tws").json()
        weatherXml = requests.get('http://www.kma.go.kr/wid/queryDFS.jsp?gridx=' + x +'&gridy=' + y)

        root = ET.fromstring(weatherXml.text).find('body')

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

    except:

        print('except')
        all_machine_count = 0
        on_machine_count = 0

    print(type(weatherList), 'list')

    title = 'Dashboard'

    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)

    variables = {'title':title, 'totalOrder':totalOrder, 'pendingOrder':pendingOrder, 'progressOrder':progressOrder, 'compOrder':compOrder, 'designOrderList': designOrderList, 'all_machine_count':all_machine_count, 'on_machine_count':on_machine_count, 'weatherList': weatherList, 'ts': ts, 'now': now, 'tomorrow': tomorrow, 'orderList':orderList}

    return render(request, 'index.html', variables)

def logout_site(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/')
def server(request):

    return render(request, 'server.html', {})
