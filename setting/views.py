#-*- coding:utf-8 -*-

import json
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from order.models import *
from account.models import User, Company, Department, Account

@csrf_exempt
def getAddress(request):
    type = int(request.POST['type'])
    code = request.POST['code']

    jsonObj = {}
    jsonList = []

    if type == 1:
        requestList = requests.get('http://www.kma.go.kr/DFSROOT/POINT/DATA/mdl.' + code + '.json.txt')
        requestList.encoding = 'utf-8'
        requestList = requestList.json()

        for obj in requestList:
            newObj = {k: v for k, v in obj.items()}
            jsonList.append(newObj)

        jsonObj = {'type': type, 'addressList': jsonList}
    elif type == 2:
        requestList = requests.get('http://www.kma.go.kr/DFSROOT/POINT/DATA/leaf.' + code + '.json.txt')
        requestList.encoding = 'utf-8'
        requestList = requestList.json()

        for obj in requestList:
            newObj = {k: v for k, v in obj.items()}
            jsonList.append(newObj)

        jsonObj = {'type': type, 'addressList': jsonList}

    return HttpResponse(json.dumps(jsonObj),content_type='application/json')

@login_required(login_url='/')
def setting(request):
    title = 'Setting'

    jsonList = []
    orderList = Order.objects.all()
    requestList = requests.get('http://www.kma.go.kr/DFSROOT/POINT/DATA/top.json.txt')
    requestList.encoding = 'utf-8'
    requestList = requestList.json()
    #print('encoding: ' + aaaaa)
    #print(requestList[0].encode('iso-8859-1').decode('utf8'), 'aaaaa')

    for obj in requestList:
        newObj = {k: v for k, v in obj.items()}
        jsonList.append(newObj)


    for obj in jsonList:
        for k, v in obj.items():
            print(k, ': ', v)

    userList = User.objects.all()

    departmentList = Department.objects.all()
    company = Company.objects.get(id=1)
    accountlist = Account.objects.all()
    return render(request, 'setting.html', {'title':title, 'company':company, 'departmentList':departmentList, 'userList':userList, 'addressList':jsonList, 'orderList':orderList, 'accountlist':accountlist, 'userlang':request.user})

def changePassword(request):
    user = request.user
    if request.method == "POST":
        password = request.POST['password']
        change_password = request.POST['change_password']
        if user.check_password(password):
            user.set_password(change_password)
            user.save()

            user = authenticate(username=user.username, password=change_password)

            if user is not None:
                login(request, user)

                return redirect('/setting')

    return redirect('/setting')


def changeUserInfo(request):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)

        #img = request.POST['img']
        name = request.POST['user_name']
        email = request.POST['user_email']

        user.name = name
        user.email = email
        try:
            propic = request.FILES['user_propic']
            user.propic = propic
        except:
            pass

        user.save()

    return redirect('/setting')

def companyInfo(request):
    if request.method == "POST":
        company = Company.objects.get(id=1)
        try:
            companyName = request.POST['company']
            company.name = companyName
        except:
            pass

        try:
            company_code = request.POST['company_code']
            company.code = company_code
        except:
            pass
        try:
            company_num = request.POST['company_num']
            company_num = company_num
        except:
            pass

        try:
            machineyn = int(request.POST['machineyn'])
            print(machineyn)
            if machineyn == 1:
                company.machineyn = True
            else:
                company.machineyn = False
        except:
            pass

        try:
            x = int(request.POST['x'])
            company.x = x
        except:
            pass

        try:
            y = int(request.POST['y'])
            company.y = y
        except:
            pass

        company.save()

    return redirect('/setting')

@csrf_exempt
def activeUser(request):

    uid = request.POST['id']

    try:
        active = User.objects.get(id=uid)

        active.is_active = True

        active.save()

        return HttpResponse(json.dumps({'success':True}), content_type='application/json')
    except:
        return HttpResponse(json.dumps({'success':False}), content_type='application/json')

@csrf_exempt
def usetdetailtest(request, id):
    userdata = {}
    if id != None:
        user = User.objects.get(id=id)
        userdata['deusername'] = user.username
        userdata['dename'] = user.name
        userdata['delevel'] = user.level
        userdata['deemail'] = user.email
        userdata['dephone'] = user.phone
        userdata['deuserdid'] = id
        if user.propic != '':
            userdata['deuserimg'] = user.propic.url
        else:
            userdata['deuserimg'] = '/static/image/ningen.png'
    return HttpResponse(json.dumps({'user': userdata}), content_type='application/json')

@csrf_exempt
def userupdates(request):
    userid = request.POST['userid']
    userdlevel = request.POST['userlevel']
    userdphone = request.POST['userdphone']
    userdemail = request.POST['userdemail']
    if userid != None:
        user = User.objects.get(id=userid)
        user.level = userdlevel
        user.phone = userdphone
        user.email = userdemail

        user.save()
    return redirect('/setting')

@csrf_exempt
def userdel(request):
    userid = request.POST['userid']
    if userid != None:
        user = User.objects.get(id=userid)
        user.delete()
    return redirect('/setting')


@csrf_exempt
def accountadd(request):
    accountname = request.POST['accountname']
    accountmanage = request.POST['accountmanage']
    accountwork = request.POST['accountwork']
    accounttype = request.POST['accounttype']
    accountnum = request.POST['accountnum']
    accountaddress = request.POST['accountaddress']
    if accountname == '':
        msg = '거래처 명을 입력해주세요'
        return render(request, 'msg/errorPage.html', {'msg': msg})
    if accountmanage == '':
        msg = '거래처 담당자명을 입력해주세요'
        return render(request, 'msg/errorPage.html', {'msg': msg})
    if accountnum == '':
        msg = '거래처 사업자 등록번호를 입력해주세요'
        return render(request, 'msg/errorPage.html', {'msg': msg})
    if accountname !='' and accountmanage !='' and accountnum !='':
        Account.objects.create(accountname=accountname,accountmanager=accountmanage,
                           accountwork=accountwork,accounttype=accounttype,accountnum=accountnum,accountaddress=accountaddress)

        msg = '거래처가 등록 되었습니다'
        return render(request, 'msg/errorPage.html', {'msg': msg})


#거래처 정보 불러오기
@csrf_exempt
def accountselect(request):
    if request.method == "POST":
        accountdata = {}
        accountid = request.POST['accountid']
        if accountid != '':
            account = Account.objects.get(id=accountid)
            accountdata['accountid'] = account.id
            accountdata['accountname'] = account.accountname
            accountdata['accountnum'] = account.accountnum
            accountdata['accountwork'] = account.accountwork
            accountdata['accountaddress'] = account.accountaddress
            accountdata['accountmanager'] = account.accountmanager
            accountdata['accounttype'] = account.accounttype

            return HttpResponse(json.dumps({'accountinfo': accountdata}), content_type='application/json')

@csrf_exempt
def accountmodify(request):
    accountid = request.POST['accountidd']
    accountname = request.POST['accountname']
    accountmanage = request.POST['accountmanage']
    accountwork = request.POST['accountwork']
    accountnum = request.POST['accountnum']
    accounttype = request.POST['accounttype']
    accountaddress = request.POST['accountaddress']
    if accountid != None:
        account = Account.objects.get(id=accountid)
        account.accountname = accountname
        account.accountmanager = accountmanage
        account.accountwork = accountwork
        account.accountnum = accountnum
        account.accounttype = accounttype
        account.accountaddress = accountaddress

        account.save()
        return redirect('/setting')

@csrf_exempt
def accountdel(request):
    accountids = request.POST['accountid']
    if accountids != None:
        account = Account.objects.get(id=accountids)
        account.delete()

    return redirect('/setting')
@csrf_exempt
def langch(request):
    try:
        lang = request.POST['lang']
        user = request.user
        user.lang_code = lang
        user.save()
        return HttpResponse(json.dumps({'success':True}), content_type='application/json')
    except:
        return HttpResponse(json.dumps({'success': False}), content_type='application/json')


