#-*- coding:utf-8 -*-

import json
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from order.models import *
from account.models import User, Company, Department

@csrf_exempt
def getAddress(request):
    type = int(request.POST['type'])
    code = request.POST['code']

    jsonObj = {}
    jsonList = []

    if type == 1:
        print('2')
        requestList = requests.get('http://www.kma.go.kr/DFSROOT/POINT/DATA/mdl.' + code + '.json.txt')
        requestList.encoding = 'utf-8'
        requestList = requestList.json()

        for obj in requestList:
            newObj = {k: v for k, v in obj.items()}
            jsonList.append(newObj)

        jsonObj = {'type': type, 'addressList': jsonList}
    elif type == 2:
        print('2')
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
    print('12121212121212 : ', requestList.encoding)
    requestList.encoding = 'utf-8'
    requestList = requestList.json()
    #print('encoding: ' + aaaaa)
    #print(requestList[0].encode('iso-8859-1').decode('utf8'), 'aaaaa')

    for obj in requestList:
        print('obj : ', obj)
        newObj = {k: v for k, v in obj.items()}
        jsonList.append(newObj)


    for obj in jsonList:
        for k, v in obj.items():
            print(k, ': ', v)

    od = Order.objects.all()
    userList = User.objects.all()

    departmentList = Department.objects.all()
    company = Company.objects.get(id=1)
    return render(request, 'setting.html', {'title':title, 'company':company, 'departmentList':departmentList, 'userList':userList, 'addressList':jsonList, 'orderList':orderList})

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

        img = request.POST['img']
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

def createDepartment(request):

    department = request.POST['department']
    if department != '':
        Department(name=department).save()
        return redirect('/setting')

    elif department == '':
        msg = '부서명을 입력해주세요.'
        return render(request, 'msg/errorPage.html', {'msg': msg})


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