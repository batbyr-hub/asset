# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import *
import logging
from datetime import datetime, timedelta
import json, base64, requests
from Crypto.Cipher import DES3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from ctypes import *
# import urllib
from urllib.parse import quote_plus
import hashlib
import os
import random
import string
from django.core.paginator import Paginator
from django.http import HttpResponse
# import StringIO
try:
    import StringIO
except ImportError:
    from io import StringIO
import xlsxwriter
from django.db.models import Q
# from threading import Timer
from rest_framework.decorators import api_view
import socket
from rest_framework.response import Response
import time
import threading


log_date = datetime.now().strftime('%Y-%m-%d')
# log_file = 'Logs/Log_{0}'.format(log_date)
log_file = 'C:/Users/batuu/OneDrive/Documents/Self-employed/Projects/asset/Logs/Log_{0}'.format(log_date)
logging.basicConfig(filename=log_file + '.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

x = datetime.today()
y = x.replace(day=x.day, hour=8, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t = y - x
secs = delta_t.total_seconds()


# id = models.AutoField('id', primary_key=True, db_index=True)
# AssetPackageData, Department, Jobposition

# Create your views here.
# http://192.168.200.216:8080/
def login(request):
    logging.info("login")
    if "user_id" in request.GET:
        user_id = request.GET["user_id"]
        employee = Employee.objects.get(user_id=user_id, status='A')
        if AssetPermission.objects.filter(employee_id=employee.id, status='A').exists():
            assper = AssetPermission.objects.get(employee_id=employee.id, status='A')
            assper.confirmed = "no"
            assper.save()
            # simper = SimplePermission.objects.get(employee_id=employee.id, status='A')
            # simper.confirmed = "no"
            # simper.save()
    return render(request, 'login.html')


def nuur(request):
    logging.info("Nuur")

    if "user_id" in request.GET:
        logging.info("GET")
        user_id = request.GET["user_id"]
        employee = Employee.objects.get(user_id=user_id, status='A')
        user = User.objects.get(user_id=user_id)
        acceso = "no"
        tipo = ""
        assper = ""
        filter_acceso = "no"
        logging.info("employee id")
        logging.info(employee.id)
        if AssetPermission.objects.filter(employee_id=employee.id, status='A').exists():
            assper = AssetPermission.objects.get(employee_id=employee.id, status='A')
            if assper.confirmed == "no":
                # 303 tusgai dugaaraar batalgaajuulah code ilgeene
                url = "http://192.88.80.199/cgi-bin/sendsms?username=javxa&password=javxa123&to=" + str(
                    user.mobile) + "&text=" + str(assper.confirmation)
                hariu = requests.get(url)
                logging.info(hariu.content)
            tipo = request.GET["tipo"]
            acceso = "yes"
            # context = {"user_id": user_id, "assper": assper, "acceso": "yes", "name": employee.name, "tipo": tipo}
            # return render(request, "nuur.html", context)
        # else:
        if NfilterPermission.objects.filter(user_id=user_id, status='A').exists():
            filter_acceso = "yes"
        # else:

            # logging.error("Уучлаарай та нэвтрэх эрхгүй байна")
        # context = {"error": "Уучлаарай та нэвтрэх эрхгүй байна", "user_id": user_id, "acceso": acceso,
        #            "name": employee.name}
        logging.info("ACCESO")
        logging.info(acceso)
        context = {"user_id": user_id, "assper": assper, "acceso": acceso, "name": employee.name, "tipo": tipo, "filter_acceso": filter_acceso}
        return render(request, 'nuur.html', context)
    else:
        # res = updateTables(180)

        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        logging.info(username)
        # logging.info(password)

        res = checkUser(username, password)
        logging.info(res.content)
        result = json.loads(res.content)
        logging.info(result["errorCode"])

        if result["errorCode"] == "0000":
            user_id = Decrypt(result["user_id"])
            employee = Employee.objects.get(user_id=user_id, status='A')
            # logging.info(employee.id)
            acceso = "yes"
            filter_acceso = "no"
            assper = ""
            if AssetPermission.objects.filter(employee_id=employee.id, status='A').exists():
                confirmation = get_random_alphanumeric_string(6)
                # logging.info(confirmation)
                assper = AssetPermission.objects.get(employee_id=employee.id, status='A')
                assper.confirmation = confirmation
                assper.save()
                acceso = "no"
                # context = {"user_id": user_id, "name": employee.name, "assper": assper, "acceso": "no"}
            if NfilterPermission.objects.filter(user_id=user_id, status='A').exists():
                logging.info("NfilterPermission_acceso")
                filter_acceso = "yes"
                # context = {"user_id": user_id, "name": employee.name, "acceso": "yes"}
            # else:
            #     logging.info("EEELLLSSSEEE")
            #     context = {"user_id": user_id, "name": employee.name, "acceso": "no"}
            logging.info("ACCESO "+str(acceso))
            context = {"user_id": user_id, "name": employee.name, "assper": assper, "acceso": acceso, "filter_acceso": filter_acceso}
            return render(request, "nuur.html", context)
        else:
            context = {"error": "Нэр эсвэл нууц үг буруу байна"}
            return render(request, 'login.html', context)


def niitShaardah(request):
    logging.info("Niit shaardah huudas")
    user_id = request.GET["user_id"]
    tipo = request.GET["tipo"]
    page_number = request.GET['page']

    employee = Employee.objects.get(user_id=user_id, status='A')
    logging.info(user_id)
    assetPermission = AssetPermission.objects.get(user_id=user_id)
    level = int(assetPermission.level) - 1
    status = "2"
    if assetPermission.level == "1":
        level = "1"
        status = "0"
        assetFirm = AssetFirmData.objects.filter(
        Q(userid=AssetPermission.objects.get(status='A', level=str(level)).id, status=0) | Q(
            userid=AssetPermission.objects.get(status='A', level=str(level)).id, status=2)).order_by('status', '-id')
    # logging.info(level)
    else:
        assetFirm = AssetFirmData.objects.filter(userid=AssetPermission.objects.get(status='A', level=str(level)).id, status=status).order_by('status', '-id')

        # assetFirm = AssetFirmData.objects.filter(Q(userid=assetPermission.id) | Q(
        #     userid=AssetPermission.objects.get(status='A', level=str(level)).id, status=status)).order_by('status', '-id')

        # assetFirm = AssetFirmData.objects.filter(userid=AssetPermission.objects.get(status='A', level=str(level)).id,
        #     status=status).filter(userid=assetPermission.id).order_by('status', '-id')
    # logging.info("ASSETFIRM")
    # for i in range(len(assetFirm)):
    #     logging.info(assetFirm[i].assetpackagedataid)
    # logging.info("ASSETFIRM LENGHT")
    # logging.info(len(assetFirm))
    count = assetFirm.filter(status=0).count()
    logging.info(count)
    # logging.info(assetFirm[1].assetpackagedataid)
    # logging.info(AssetPermission.objects.get(user_id=user_id).id)
    # logging.info(AssetFirmData.objects.get(assetpackagedataid=assetFirm[1].assetpackagedataid, userid=AssetPermission.objects.get(user_id=user_id).id).status)
    wrong_token = ""
    if "token" in request.POST:
        token = request.POST["token"]
        assper = AssetPermission.objects.get(employee_id=employee.id, status='A')
        if assper.confirmation == token:
            assper.confirmed = "yes"
            assper.confirmed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            assper.save()
        else:
            wrong_token = "Баталгаажуулах код буруу байна!"
            context = {"user_id": user_id, "assper": assper, "wrong_token": wrong_token, "acceso": "yes"}
            return render(request, "nuur.html", context)

    pagination = 20
    minor = (int(page_number) - 1) * pagination
    if int(len(assetFirm) / pagination) == int(page_number) - 1:
        mayor = len(assetFirm)
    else:
        mayor = int(page_number) * pagination

    logging.info(minor)
    logging.info(mayor)

    dat = []
    for i in range(minor, mayor):
        if AssetPackageData.objects.filter(id=assetFirm[i].assetpackagedataid, status='A').exists():
            if AssetFirmData.objects.filter(assetpackagedataid=assetFirm[i].assetpackagedataid, userid=AssetPermission.objects.get(user_id=user_id).id).exists():
                da = AssetPackageData.objects.get(id=assetFirm[i].assetpackagedataid, status='A')
                dat.append({
                    "id": da.id,
                    "assetslipid": da.assetslipid,
                    "zoriulalt": da.reasonvalue,
                    "userto": da.userto,
                    "ognoo": da.createddate,
                    "tuluv": AssetFirmData.objects.get(assetpackagedataid=assetFirm[i].assetpackagedataid, userid=AssetPermission.objects.get(user_id=user_id).id).status
                })
    logging.info("DAT")
    for i in range(len(dat)):
        logging.info(dat[i])

    paginator = Paginator(assetFirm, pagination)
    logging.info(paginator)
    page_obj = paginator.page(page_number)
    logging.info(page_obj)

    context = {"assetslipids": dat, "user_id": user_id, "tipo": tipo, "count": count,
               "employee_name": employee.name, "page_obj": page_obj}
    return render(request, "asset/niitShaardah.html", context)


def huleegdejBaigaa(request):
    logging.info("Huleegdej baigaa")
    user_id = request.GET["user_id"]
    tipo = request.GET["tipo"]
    assetPackageDataId = request.GET["assetPackageDataId"]
    page = request.GET["page"]

    user = User.objects.get(user_id=user_id)
    # assetFirm = AssetFirmData.objects.get(assetpackagedataid=assetPackageDataId, userid=AssetPermission.objects.get(user_id=user_id).id)
    assetFirm = AssetFirmData.objects.filter(assetpackagedataid=assetPackageDataId)
    logging.info("ASSETFIRM")
    logging.info(assetFirm)
    # assetttt = AssetFirmData.objects.get(assetpackagedataid=assetPackageDataId, userid=13)
    # logging.info(assetttt)
    # logging.info(assetttt.status)
    # logging.info(assetttt.userid)
    # assetFirm.status = 1
    # assetFirm.save()

    packageData = AssetPackageData.objects.get(id=assetPackageDataId)
    detailsData = AssetDetailsData.objects.filter(assetslipid=packageData.assetslipid)
    code = packageData.uploadfile
    if code != None:
        # with open(os.path.expanduser('static/attachment/' + str(id_asset) + '.pdf'), 'wb') as fout:
        with open(os.path.expanduser('home/bam/asset/static/attachment/' + str(assetPackageDataId) + '.pdf'), 'wb') as fout:
            fout.write(base64.decodestring(code))

    assn = packageData.locationto
    if "=" in assn:
        aimag = assn.split("=")[0]
        sum = assn.split("=")[1]
        saitiinNer = assn.split("=")[2]
    else:
        aimag = assn.split("-")[0]
        sum = assn.split("-")[1]
        saitiinNer = assn.split("-")[2]

    # logging.info(assetFirm)
    context = {"aimag": aimag, "sum": sum, "saitiinNer": saitiinNer, "detailsData": detailsData, "user_id": user_id,
               "tipo": tipo, "packageData": packageData, "user": user, "page": page, "assetFirm": assetFirm}
    return render(request, "asset/huleegdejBaigaa.html", context)


def hyanasan(request):
    logging.info("HYANASAN")
    assetPackageDataId = request.GET["assetPackageDataId"]
    zuvshuursun = ""
    if "tuluv" in request.POST:
        zuvshuursun = request.POST["tuluv"]
    user_id = request.GET["user_id"]
    tipo = request.GET["tipo"]
    page = request.GET["page"]

    if request.method == 'POST':
        assetFirm = AssetFirmData.objects.get(assetpackagedataid=assetPackageDataId,
                                              userid=AssetPermission.objects.get(user_id=user_id).id)
        if zuvshuursun == "yes":
            assetFirm.status = 2
        if zuvshuursun == "no":
            assetFirm.status = 3
        assetFirm.save()

        url = "http://192.168.18.232/GAgent/AssetChecked.asmx/CheckedAsset"
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        da = {
            "assetslipid": AssetPackageData.objects.get(id=assetPackageDataId).assetslipid,
            "firmer": user_id,
            "status": assetFirm.status
        }
        logging.info(da)
        hariu = requests.post(url, data=da, headers=headers)
        # logging.info(hariu.content)
        result = json.loads(hariu.content)
        logging.info(result)
        # logging.info(str(albanTushaal) + " " + str(assetslipid) + " " + result["status"])

        notification = str(assetPackageDataId) + " дугаартай шаардах зөвшөөрөгдөж амжилттай хадгалагдлаа"
        context = {"user_id": user_id, "tipo": tipo, "page": page, "notification": notification}
        return render(request, "notification.html", context)



# ==================== Engiin shaardah ===============================


def choose(request):
    logging.info("CHOOSE")
    user_id = request.GET["user_id"]
    tipo = request.GET["tipo"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    simper = ""
    error = ""
    logging.info(employee.id)
    if SimplePermission.objects.filter(employee_id=employee.id, status='A').exists():
        simper = "second_third"
    else:
        logging.info(employee.job_position_id)
        if Jobposition.objects.filter(id=employee.job_position_id).exists():
            job_position = Jobposition.objects.get(id=employee.job_position_id)
            if job_position.level_group_id != None:
                logging.info(job_position.level_group_id)
                logging.info(Department.objects.get(id=employee.department_id).sign_leader_id)
                if (job_position.level_group_id == 3 and Department.objects.get(
                        id=employee.department_id).sign_leader_id != "") or (checkAlternates(user_id) == 3):
                    simper = "first"
                    logging.info("GGGGGGGGGGGGGGGGGG")
                else:
                    logging.info("DDDDDDDDDDDD")
            else:
                logging.info("jobposition level group none")
        else:
            error = "Таны албан тушаал олдсонгүй. Хүний нөөцийн менежертээ хандана уу"
    logging.info(simper)
    simtre = ""
    if SimpleTreasurers.objects.filter(employee_id=employee.id, status='A').exists():
        simtre = SimpleTreasurers.objects.get(employee_id=employee.id, status='A')
    if "token" in request.POST:
        token = request.POST["token"]
        assper = AssetPermission.objects.get(employee_id=employee.id, status='A')
        if assper.confirmation == token:
            assper.confirmed = "yes"
            assper.confirmed_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            assper.save()
        else:
            wrong_token = "Баталгаажуулах код буруу байна!"
            context = {"user_id": user_id, "assper": assper, "wrong_token": wrong_token, "acceso": "yes"}
            return render(request, "nuur.html", context)
    context = {"user_id": user_id, "employee": employee, "tipo": tipo, "simper": simper, "simtre": simtre, "error": error}
    return render(request, "simple/choose.html", context)


def checkAlternates(user_id):
    logging.info("checkAlternates")
    employee = Employee.objects.get(user_id=user_id, status='A')
    logging.info(employee.id)
    if EmployeeAlternates.objects.filter(alternate_employee_id=employee.id).exists():
        logging.info("Orloj bgaa")
        empAlt_employee_id = EmployeeAlternates.objects.get(alternate_employee_id=employee.id).employee_id
        logging.info(empAlt_employee_id)
        emp_job_position_id = Employee.objects.get(id=empAlt_employee_id).job_position_id
        job_position = Jobposition.objects.get(id=emp_job_position_id).level_group_id
        logging.info(job_position)
        return job_position
    else:
        return None


def firstOrThird(request):
    user_id = request.GET["user_id"]
    tipo = request.GET["tipo"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    context = {"user_id": user_id, "employee": employee, "tipo": tipo}
    return render(request, "simple/firstOrThird.html", context)


def form(request):
    logging.info("form")
    user_id = request.GET["user_id"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    jobposition = Jobposition.objects.get(id=employee.job_position_id)
    date = datetime.now().strftime('%Y он %m сар %d-ны өдөр'.encode('utf-8'))
    products = SimpleProducts.objects.all()
    treasures = SimpleTreasurersType.objects.all()
    turul = []
    if "nyarav_id" in request.GET:
        nyarav_id = request.GET["nyarav_id"]
        types = SimpleProductsType.objects.filter(treasurers_id=nyarav_id)
        for i in range(len(types)):
            turul.append(types[i].type)
    companies = Company.objects.all()
    context = {"user_id": user_id, "employee": employee, "date": date, "jobposition": jobposition, "products": products, "treasures": treasures, "types": turul, "companies": companies}
    return render(request, "simple/form.html", context)


def info(request):
    logging.info("info")
    nyarav_id = request.GET["nyarav_id"]
    types = SimpleProductsType.objects.filter(treasurers_id=nyarav_id)
    turul = []
    for i in range(len(types)):
        turul.append(types[i].type)
    logging.info(turul)
    return HttpResponse(json.dumps(turul), content_type="application/json")


def infoCompany(request):
    logging.info("infoCompany")
    company_id = request.GET["company_id"]
    if company_id == "3":
        treasurers = SimpleTreasurers.objects.filter(treasurer_type_id=1, status='A')
        # treasurers.append(SimpleTreasurers.objects.filter(treasurer_type_id=5, status='A'))
    elif company_id == "2":
        treasurers = SimpleTreasurers.objects.filter(company_id=company_id, status='A')
    else:
        treasurers = SimpleTreasurers.objects.all().filter(status='A')
    turul = []
    for i in range(len(treasurers)):
        turul.append({
            "id": treasurers[i].id,
            "name": treasurers[i].first_name
        })
    logging.info(turul)
    return HttpResponse(json.dumps(turul), content_type="application/json")


def getProducts(request):
    logging.info("getProducts")
    nyarav_id = request.GET["nyarav_id"]
    turul = request.GET["turul"]
    turul_id = SimpleProductsType.objects.get(treasurers_id=nyarav_id, type=turul).id
    names = SimpleProducts.objects.filter(nyaraviinturul=nyarav_id, turul=turul_id, status='A')
    ner = []
    for i in range(len(names)):
        ner.append(names[i].ner)
    return HttpResponse(json.dumps(ner), content_type="application/json")


def saveForm(request):
    logging.info("SAVE FORM")
    user_id = request.GET["user_id"]
    productName = request.POST.getlist('product[]')
    desiredsize = request.POST.getlist('hussen[]')
    nyarav = request.POST["nyarav"]
    turul = request.POST["turul"]
    company = request.POST["company"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    dpt = Department.objects.get(id=employee.department_id)
    jobposition = Jobposition.objects.get(id=employee.job_position_id).name
    # minor = 0
    packageData = SimplePackageData()
    packageData.userid = user_id
    packageData.username = employee.surname + " " + employee.name + ", " + jobposition
    if dpt.parent_id == 1:
        packageData.headid = dpt.sign_leader_id
    else:
        if Department.objects.get(id=dpt.parent_id).sign_leader_id == None:
            depart = Department.objects.get(id=dpt.parent_id).parent_id
            packageData.headid = Department.objects.get(id=depart).sign_leader_id
        else:
            packageData.headid = Department.objects.get(id=dpt.parent_id).sign_leader_id
    packageData.createddate = datetime.now().strftime("%Y-%m-%d")
    packageData.haana = request.POST["haana"]
    packageData.purpose = request.POST["zoriulalt"]
    packageData.firstfirm = 0
    packageData.secondfirm = 0
    packageData.thirdfirm = 0
    packageData.status = "A"
    packageData.treasurer = nyarav
    packageData.company_id = company
    packageData.save()
    for n in range(0, len(productName)):
        if productName[n] != "" or desiredsize[n] != "":
            detailsData = SimpleDetailsData()
            detailsData.packagecode = packageData.packagecode
            detailsData.productname = productName[n]
            if SimpleProducts.objects.filter(ner=productName[n], status='A').exists():
                product = SimpleProducts.objects.get(ner=productName[n], status='A')
                detailsData.productcode = product.diamondcode
                detailsData.unit = product.hemjihnegj
            detailsData.desiredsize = desiredsize[n]
            # if n == 0:
            #     minor = data.id
            # data.packagecode = minor
            detailsData.save()
    notification = "Таны " + str(packageData.packagecode) + " дугаартай шаардах амжилттай үүслээ"
    context = {"user_id": user_id, "notification": notification, "employee": employee}
    return render(request, "notification.html", context)


def simpleNiitShaardah(request):
    logging.info("simpleNiitShaardah")
    user_id = request.GET["user_id"]
    page_number = request.GET['page']
    employee = Employee.objects.get(user_id=user_id, status='A')

    position = ""
    d1 = ""
    if Department.objects.filter(id=employee.department_id, status='A').exists():
        d1 = Department.objects.get(id=employee.department_id, status='A')
        logging.info(d1.parent_id)
        if d1.parent_id == 1:
            sign_leader_id = d1.sign_leader_id
        else:
            while d1.parent_id != 1:
                d1 = Department.objects.get(id=d1.parent_id, status='A')

                if d1.parent_id == 1:
                    sign_leader_id = d1.sign_leader_id
                    break
            # logging.info(d1.parent_id)
            # sign_leader_id = Department.objects.get(id=d1.parent_id, status='A').sign_leader_id
        logging.info("sign_leader_id")
        logging.info(sign_leader_id)
        if checkAlternates(user_id) == 3:
            position = "firstfirm"

    simple_permission = ""
    logging.info("position1")
    logging.info(position)

    if "position" in request.GET:
        position = request.GET["position"]
    logging.info("position2")
    logging.info(position)
    if position == "firstfirm" or position == "thirdfirm":
        position = position
    else:
        sim_per = 0
        if SimplePermission.objects.filter(employee_id=employee.id, status='A').exists():
            simple_permission = SimplePermission.objects.get(employee_id=employee.id, status='A')
            if simple_permission.level == 2:
                position = "secondfirm"
                sim_per = 2
            # if simple_permission.employee_id == 545:
            #     position = "thirdfirm"
        if Jobposition.objects.filter(id=employee.job_position_id).exists():
            jobposition = Jobposition.objects.get(id=employee.job_position_id).level_group_id
        else:
            jobposition = ""
        if d1.parent_id == 1 and d1.status == "A" and jobposition == 3:
            position = "firstfirm"
            if sim_per == 2:
                position = "secondfirm"
    logging.info("position3")
    logging.info(position)

    # if employee.id == 1368:
    #     position = "secondfirm"
        # if position == "firstfirm":
            # position = "firstfirm"
        # else:

    # logging.info("position")
    # logging.info(position)

    arr1 = ""
    owner = ""
    if "my" in request.GET and request.GET["my"] == "my":
        logging.info("my")
        arr1 = SimplePackageData.objects.filter(status='A', userid=user_id).values_list('packagecode', flat=True).order_by('-packagecode')
        position = "thirdfirm"
        owner = "my"
    else:
        if position == "firstfirm":
            arr1 = SimplePackageData.objects.filter(status='A', headid=sign_leader_id).values_list('packagecode', flat=True).order_by('firstfirm', '-packagecode')
        if position == "secondfirm":
            arr1 = SimplePackageData.objects.filter(status='A', firstfirm=2).values_list('packagecode', flat=True).order_by('secondfirm', '-packagecode')
        if position == "thirdfirm":
            arr1 = SimplePackageData.objects.filter(status='A', secondfirm=2).values_list('packagecode', flat=True).order_by('thirdfirm', '-packagecode')
    logging.info(arr1)

    count = 0
    # count1 = 0
    for i in range(len(arr1)):
        d = SimplePackageData.objects.filter(packagecode=arr1[i])
        if d.values(position)[0][position] == "0":
            count += 1
        # if d.values(position)[0][position] == "2":
        #     count1 += 1

    pagination = 20
    minor = (int(page_number) - 1) * pagination
    if int(len(arr1) / pagination) == int(page_number) - 1:
        mayor = len(arr1)
    else:
        mayor = int(page_number) * pagination

    arr5 = []
    for i in range(minor, mayor):
        d = SimplePackageData.objects.filter(packagecode=arr1[i])
        da = d[0]
        if da.status == 'A':
            arr5.append({
                "packagecode": da.packagecode,
                "zoriulalt": da.purpose,
                "userto": da.username,
                "ognoo": da.createddate,
                "tuluv": d.values(position)[0][position],
                "first0": da.firstfirm
            })
        # logging.info(d.values(position)[0][position])
    logging.info("COUNT")
    logging.info(count)
    logging.info(arr5)

    paginator = Paginator(arr1, pagination)
    page_obj = paginator.page(page_number)

    if owner == "my":
        position = ""

    context = {"employee": employee, "datas": arr5, "user_id": user_id, "page_obj": page_obj, "count": count,
               "position": position, "owner": owner}
    return render(request, "simple/simpleNiitShaardah.html", context)


def deleteShaardah(request):
    logging.info("deleteShaardah")
    packageCode = request.GET["packageCode"]
    user_id = request.GET["user_id"]
    packageData = SimplePackageData.objects.get(packagecode=packageCode)
    packageData.status = "D"
    packageData.save()
    deleted = []
    deleted.append({
        "user_id": user_id,
        "tipo": "2",
        "notification": "Amjilttai ustgagdlaa"
    })
    return HttpResponse(json.dumps(deleted), content_type="application/json")


def firm(request):
    logging.info("firm")
    user_id = request.GET["user_id"]
    package_id = request.GET["package_id"]
    owner = request.GET["owner"]
    position = request.GET["position"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    packageData = SimplePackageData.objects.get(packagecode=package_id)
    detailsData = SimpleDetailsData.objects.filter(packagecode=package_id)
    headName = Employee.objects.get(id=packageData.headid).name
    company = ""
    if packageData.company_id != "":
        company = Company.objects.get(id=packageData.company_id).name
    context = {"user_id": user_id, "employee": employee, "detailsData": detailsData, "packageData": packageData, "position": position, "headName": headName, "owner": owner, "company": company}
    return render(request, "simple/firm.html", context)


def firmed(request):
    logging.info("firmed")
    user_id = request.GET["user_id"]
    package_id = request.GET["package_id"]
    position = request.GET["position"]
    firmado = request.POST["firmado"]
    if "zuvshuursun[]" in request.POST:
        secondFirmConfirmed = request.POST.getlist('zuvshuursun[]')
        detailsData = SimpleDetailsData.objects.filter(packagecode=package_id)
        for i in range(len(detailsData)):
            detailsData[i].allowedsize = secondFirmConfirmed[i]
            detailsData[i].save()
    tailbar = request.POST["tailbar"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    data = SimplePackageData.objects.get(packagecode=package_id)
    hariu = ""
    if firmado == "yes":
        if position == "firstfirm":
            data.firstfirm = 2
            data.firstfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.firstfirmdescription = tailbar
        if position == "secondfirm":
            data.secondfirm = 2
            data.secondfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.secondfirmdescription = tailbar
        if position == "thirdfirm":
            # data.secondfirm = 2
            # data.secondfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # data.secondfirmdescription = tailbar
            data.thirdfirm = 2
            data.thirdfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.thirdfirmdescription = tailbar
        hariu = "зөвшөөрөгдөж"
    if firmado == "no":
        if position == "firstfirm":
            data.firstfirm = 3
            data.firstfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.firstfirmdescription = tailbar
        if position == "secondfirm":
            data.secondfirm = 3
            data.secondfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.secondfirmdescription = tailbar
        if position == "thirdfirm":
            # data.secondfirm = 3
            # data.secondfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # data.secondfirmdescription = tailbar
            data.thirdfirm = 3
            data.thirdfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data.thirdfirmdescription = tailbar
        hariu = "татгалзаж"
    data.save()

    logging.info(str(data.packagecode)+" "+str(firmado))
    notification = str(data.packagecode) + " дугаартай шаардах " + hariu + " амжилттай хадгалагдлаа"
    context = {"user_id": user_id, "notification": notification, "employee": employee, "tipo": "2",
               "position": position}
    return render(request, "notification.html", context)


def nyarav(request):
    logging.info("nyarav")
    user_id = request.GET["user_id"]
    page_number = request.GET['page']

    employee = Employee.objects.get(user_id=user_id, status='A')

    treasurer = SimpleTreasurers.objects.get(employee_id=employee.id).treasurer_type_id
    arr1 = SimplePackageData.objects.filter(status='A', treasurer=treasurer, thirdfirm=2).values_list('packagecode', flat=True).order_by('-packagecode')
    logging.info(arr1)

    pagination = 20
    minor = (int(page_number) - 1) * pagination
    if int(len(arr1) / pagination) == int(page_number) - 1:
        mayor = len(arr1)
    else:
        mayor = int(page_number) * pagination

    arr5 = []
    for i in range(minor, mayor):
        d = SimplePackageData.objects.filter(packagecode=arr1[i])
        da = d[0]
        if da.status == 'A':
            arr5.append({
                "id": da.packagecode,
                "zoriulalt": da.purpose,
                "userto": da.username,
                "ognoo": da.createddate
            })
    logging.info("arr5")
    logging.info(arr5)

    paginator = Paginator(arr1, pagination)
    page_obj = paginator.page(page_number)

    context = {"employee": employee, "datas": arr5, "user_id": user_id, "page_obj": page_obj}
    return render(request, "simple/nyarav.html", context)


def viewShaardah(request):
    logging.info("viewShaardah")
    user_id = request.GET["user_id"]
    package_id = request.GET["package_id"]
    page = request.GET["page"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    packageData = SimplePackageData.objects.get(packagecode=package_id)
    detailsData = SimpleDetailsData.objects.filter(packagecode=package_id)
    # simplePermission = SimplePermission.objects.filter(status='A')
    company = ""
    if packageData.company_id != "":
        company = Company.objects.get(id=packageData.company_id).name
    context = {"user_id": user_id, "employee": employee, "packageData": packageData, "detailsData": detailsData,
               "page": page, "company": company}
    return render(request, "simple/viewShaardah.html", context)


def export_page(request):
    logging.info("export_page")
    user_id = request.GET["user_id"]
    package_id = request.GET["package_id"]
    employee = Employee.objects.get(user_id=user_id, status='A')
    packageData = SimplePackageData.objects.get(packagecode=package_id)
    detailsData = SimpleDetailsData.objects.filter(packagecode=package_id)
    company = Company.objects.get(id=packageData.company_id).name
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.set_landscape()
    worksheet.set_paper(11)
    worksheet.set_margins(0.0, 0.0, 0.0, 0.0)
    line_border = workbook.add_format()
    bottom_line = workbook.add_format()
    dot_border = workbook.add_format()
    border = workbook.add_format({'border': 1})
    center = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    border_center = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    text_wrap = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'border': 1})
    font_size = workbook.add_format({'bold': True, 'font_size': 16})
    size10 = workbook.add_format({'font_size': 10})
    size14 = workbook.add_format({'bold': True, 'font_size': 14})
    line_border.set_border(1)
    bottom_line.set_bottom(1)
    dot_border.set_bottom(7)
    worksheet.set_column('A:A', 4)
    worksheet.set_column('C:C', 24)
    worksheet.set_column('D:E', 6)
    worksheet.set_column('H:J', 14)
    worksheet.write('A1', 'НХМаягт БМ-6', size10)
    worksheet.write('H1', 'Сангийн сайдын 2017 оны 12 дугаар сарын', size10)
    worksheet.write('H2', '5-ны өдрийн 347 тоот тушаалын хавсралт', size10)
    worksheet.write('B3', '', bottom_line)
    worksheet.write('C3', company, bottom_line)
    worksheet.write('D3', 'ШААРДАХ ХУУДАС №', font_size)
    worksheet.write('H3', packageData.packagecode, center)
    worksheet.write('C4', '/байгууллагын нэр/')
    createddate = packageData.createddate
    on = createddate.split('-')[0]
    sar = createddate.split('-')[1]
    udur = createddate.split('-')[2]
    worksheet.write('H5', str(on) + " он " + str(sar) + " сар " + str(udur) + "-ны өдөр")
    worksheet.write('A7', 'Хэнээс', size14)
    worksheet.merge_range('C7:J7', packageData.username, bottom_line)
    worksheet.merge_range('C8:J8', '(Овог нэр, албан тушаал)', center)
    worksheet.write('A9', 'Хаана', size14)
    worksheet.merge_range('C9:J9', packageData.haana, bottom_line)
    worksheet.merge_range('C10:J10', '(Цех, тасаг, алба)', center)
    worksheet.write('A11', 'Зориулалт', size14)
    worksheet.merge_range('C11:J11', packageData.purpose, bottom_line)
    worksheet.conditional_format('A13:J28', {'type': 'blanks', 'format': border})
    worksheet.merge_range('A13:A14', 'д/д', border_center)
    worksheet.merge_range('B13:E14', 'Материалын үнэт зүйлийн нэр', text_wrap)
    worksheet.merge_range('F13:F14', 'Код', border_center)
    worksheet.merge_range('H13:J13', 'Хэмжих нэгж', text_wrap)
    worksheet.write('I13', 'Тоо хэмжээ', border_center)
    worksheet.write('H14', 'Хүссэн', border_center)
    worksheet.write('I14', 'Зөвшөөрсөн', border_center)
    worksheet.write('J14', 'Олгосон', border_center)
    j = 15
    for i in range(len(detailsData)):
        worksheet.merge_range('B' + str(j) + ':E' + str(j), detailsData[i].productname, border_center)
        worksheet.write('F' + str(j), detailsData[i].productcode, border_center)
        worksheet.write('G' + str(j), detailsData[i].unit, border_center)
        worksheet.write('H' + str(j), detailsData[i].desiredsize, border_center)
        worksheet.write('I' + str(j), detailsData[i].allowedsize, border_center)
        j += 1
    m = 15
    n = j
    for k in range(1, 15):
        worksheet.write('A' + str(m), str(k), border_center)
        if 29 > n:
            worksheet.merge_range('B' + str(n) + ':E' + str(n), '', border_center)
        m += 1
        n += 1
    simper = SimplePermission.objects.filter(status='A')
    worksheet.write('A30', 'Зөвшөөрсөн:')
    worksheet.write('C30', 'Дарга')
    worksheet.insert_image('D30', 'home/user/asset/static/images/checked.png', {'x_scale': 0.5, 'y_scale': 0.5})
    # worksheet.write('D30', simper[0].last_name + " " + simper[0].first_name, dot_border)
    worksheet.write('E30', simper[0].last_name + " " + simper[0].first_name, dot_border)
    worksheet.write('G30', 'Олгосон нярав')
    worksheet.write('I30', '', dot_border)
    worksheet.write('J30', '', dot_border)
    worksheet.write('C31', 'Нягтлан бодогч')
    worksheet.insert_image('D31', 'home/user/asset/static/images/checked.png', {'x_scale': 0.5, 'y_scale': 0.5})
    # worksheet.write('D31', simper[1].last_name + " " + simper[1].first_name, dot_border)
    worksheet.write('E31', simper[1].last_name + " " + simper[1].first_name, dot_border)
    worksheet.write('G31', 'Хүлээн авсан')
    worksheet.write('I31', '', dot_border)
    worksheet.write('J31', '', dot_border)
    worksheet.write('C32', 'Шаардах хуудас бичсэн')
    worksheet.write('D32', packageData.username, dot_border)
    worksheet.write('E32', '', dot_border)
    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="engiin shaardah.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response


def checkAlbanTushaal(employee_id):
    id = AssetPermission.objects.get(employee_id=employee_id, status='A').id
    if id == 10:
        return "tagheltesiindarga"
    if id == 9:
        return "tagzahiral"
    if id == 11:
        return "ttgheltesiindarga"
    if id == 8:
        return "ttgzahiral"
    if id == 7:
        return "sbgzahiral"
    if id == 6:
        return "tagheltesiindarga"


def posicionAnterior(posicion):
    if posicion == "tagheltesiindarga":
        return "tagheltesiindarga"
    if posicion == "tagzahiral":
        return "tagheltesiindarga"
    if posicion == "ttgheltesiindarga":
        return "tagzahiral"
    if posicion == "ttgzahiral":
        return "ttgheltesiindarga"
    if posicion == "sbgzahiral":
        return "ttgzahiral"


def checkUser(ner, nuutsUg):
    logging.info("checkUser")

    ner = Encryptt(ner)
    nuutsUg = Encryptt(nuutsUg)

    ner = quote_plus(ner)
    nuutsUg = quote_plus(nuutsUg)

    ner = quote_plus(ner)
    nuutsUg = quote_plus(nuutsUg)

    url = "http://192.168.200.216:8080/serviceapp.php/userCheck/9/" + ner + "/" + nuutsUg + "/list.json"
    try:
        return requests.get(url=url)
    except get_errno() == 10060 or get_errno() == 10061:
        return False


# def Encryptt(data):
#     key = "n7r1vw7mi1w4g4048g4wokkkgss40kk"
#     key = key.encode('utf-8', 'strict')
#     key = hashlib.md5(key).digest()
#     key = key + key[0:8]
#
#     cipher = DES3.new(key, DES3.MODE_ECB)
#
#     pad_len = cipher.block_size - len(data) % cipher.block_size
#     data += str_repeat(chr(pad_len), pad_len)
#
#     result = cipher.encrypt(data)
#     result = base64.b64encode(result)
#     return result

def Encryptt(data):
    key = "n7r1vw7mi1w4g4048g4wokkkgss40kk"
    key = key.encode('utf-8', 'strict')
    key = hashlib.md5(key).digest()
    key = key + key[0:8]
    if isinstance(data, str):  # Convert string to bytes
        data = data.encode('utf-8')

    cipher = AES.new(key, AES.MODE_ECB)  # Ensure key is bytes too
    result = cipher.encrypt(pad(data, AES.block_size))  # Pad to fit block size
    return result


def str_repeat(char, count):
    result = ""
    for i in range(0, count):
        result += char
    return result


def Decrypt(datos):
    key = "n7r1vw7mi1w4g4048g4wokkkgss40kk"
    key = key.encode('utf-8', 'strict')
    key = hashlib.md5(key).digest()
    key = key + key[0:8]

    cipher = DES3.new(key, DES3.MODE_ECB)
    result = base64.b64decode(datos)
    result = cipher.decrypt(result)

    pad_len = ord(result[len(result) - 1])

    return result[0:len(result) - pad_len]


def get_random_alphanumeric_string(length):
    # letters_and_digits = string.ascii_letters + string.digits
    # letters = string.ascii_letters.lower()
    result_str = ''.join((random.choice(string.digits) for i in range(length)))
    return result_str


def updateTables(n=180):
    # 86400 sec = 1440 minutes = 24 hours
    # while True:
    #     time.sleep(n)
    #     logging.info("EVERY 3 MINUTES")
    headers = {'content-type': 'application/json'}

    EmployeeAlternates.objects.all().delete()
    url = "http://192.168.200.224:8089/serviceapp.php/employee/alternates/list.json"
    hariu = requests.get(url, headers)
    result = json.loads(hariu.content)
    for i in range(0, len(result)):
        employee_alternates = EmployeeAlternates()
        employee_alternates.employee_id = result[i]["employee_id"]
        employee_alternates.alternate_employee_id = result[i]["alternate_employee_id"]
        employee_alternates.start_date = result[i]["start_date"]
        employee_alternates.end_date = result[i]["end_date"]
        employee_alternates.start_time = result[i]["start_time"]
        employee_alternates.end_time = result[i]["end_time"]
        employee_alternates.save()

    url = "http://192.168.200.224:8089/serviceapp.php/department/list.json"
    hariu = requests.get(url, headers)
    result = json.loads(hariu.content)
    for i in range(0, len(result)):
        if Department.objects.filter(id=result[i]["id"]).exists():
            department = Department.objects.get(id=result[i]["id"])
        else:
            department = Department()
        department.parent_id = result[i]["parent_id"]
        department.sign_leader_id = result[i]["sign_leader_id"]
        department.leader_id = result[i]["leader_id"]
        department.name = result[i]["name"]
        department.eoffice = result[i]["eoffice"]
        department.email = result[i]["email"]
        department.status = result[i]["status"]
        department.save()

    url = "http://192.168.200.224:8089/serviceapp.php/jobposition/list.json"
    hariu = requests.get(url, headers)
    result = json.loads(hariu.content)
    for i in range(0, len(result)):
        if Jobposition.objects.filter(id=result[i]["id"]).exists():
            jobposition = Jobposition.objects.get(id=result[i]["id"])
        else:
            jobposition = Jobposition()
        jobposition.department_id = result[i]["department_id"]
        jobposition.level_group_id = result[i]["level_group_id"]
        jobposition.name = result[i]["name"]
        jobposition.fullname = result[i]["fullname"]
        jobposition.status = result[i]["status"]
        jobposition.save()

    url = "http://192.168.200.224:8089/serviceapp.php/employee/list.json"
    hariu = requests.get(url, headers)
    result = json.loads(hariu.content)
    for i in range(0, len(result)):
        if Employee.objects.filter(id=result[i]["id"]).exists():
            employee = Employee.objects.get(id=result[i]["id"])
        else:
            employee = Employee()
        employee.department_id = result[i]["department_id"]
        employee.job_position_id = result[i]["job_position_id"]
        employee.user_id = result[i]["user_id"]
        employee.family_name = result[i]["family_name"]
        employee.surname = result[i]["surname"]
        employee.name = result[i]["name"]
        employee.sex = result[i]["sex"]
        employee.birth_date = result[i]["birth_date"]
        employee.register_number = result[i]["register_number"]
        employee.image_url = result[i]["image_url"]
        employee.status = result[i]["status"]
        employee.current_state_id = result[i]["current_state_id"]
        employee.save()

    url = "http://192.168.200.216:8080/serviceapp.php/user/list/2/list.json"
    hariu = requests.get(url, headers)
    result = json.loads(hariu.content)
    for i in range(0, len(result)):
        if User.objects.filter(user_id=result[i]["user_id"]).exists():
            user = User.objects.get(user_id=result[i]["user_id"])
        else:
            user = User()
        user.user_id = result[i]["user_id"]
        user.username = result[i]["username"]
        user.mobile = result[i]["mobile"]
        user.email = result[i]["user_email"]
        user.save()

# t = Timer(secs, updateTables)
# t.start()
# thread = threading.Thread(target=updateTables, daemon=True)
# thread.start()




def dugaarShuultChoose(request):
    logging.info("------------------------------------------------------------------------------------------------")
    user_id = request.GET["user_id"]
    employee = Employee.objects.get(user_id=user_id)
    tsohoh = "no"
    logging.info(employee.department_id)
    # if NfilterPermission.objects.filter(department_id=employee.department_id) and Jobposition.objects.get(id=employee.job_position_id).level_group_id == "3":
    if NfilterPermission.objects.filter(department_id=employee.department_id).exists():
        # Jobposition.objects.get(id=employee.job_position_id).level_group_id == "2"
        # NfilterPermission.objects.filter(department_id=544).exists()
        tsohoh = "yes"
    logging.info(tsohoh)
    context = {"user_id": user_id, "tsohoh": tsohoh}
    return render(request, 'dugaarShuult/choose.html', context)


def dugaarShuult(request):
    logging.info("Dugaar shuult")
    user_id = request.GET["user_id"]
    employee = Employee.objects.get(user_id=user_id)
    tsohoh = "no"
    logging.info(NfilterPermission.objects.filter(department_id=employee.department_id))
    logging.info(Jobposition.objects.get(id=employee.job_position_id).level_group_id == "3")
    logging.info(Jobposition.objects.get(id=employee.job_position_id).level_group_id == "2")
    if NfilterPermission.objects.filter(department_id=employee.department_id) and (Jobposition.objects.get(id=employee.job_position_id).level_group_id == "3" or Jobposition.objects.get(id=employee.job_position_id).level_group_id == "2"):
        tsohoh = "yes"
    context = {"user_id": user_id, "tsohoh": tsohoh}
    return render(request, 'dugaarShuult/nuur.html', context)


def getprepix(request):
    logging.info("ДУГААРАА СОНГОЖ БУЙ ХЭСЭГ")

    # resultado = FilternumberBlockUnblock("block", "98000167", "", "7days", "54412345678", "192.168.200.251")
    user_ip = get_client_ip(request)
    logging.info("user_ip: " + str(user_ip))

    user_id = request.GET["user_id"]
    numbertype = request.GET["numbertype"]
    logging.info(numbertype)
    az = request.GET['az']
    prepost = "prepaid"
    if numbertype == "7":
        prepost = "postpaid"
    numbertypetmp = numbertype
    if numbertype == "3":
        numbertypetmp = 2
    logging.info(numbertypetmp)
    prefixes = list(Prefix.objects.filter(is_active=1, category=numbertypetmp).order_by("prefix"))
    logging.info(prefixes)
    pre = []
    for i in range(0, len(prefixes)):
        pre.append(str(prefixes[i].prefix))
    logging.info(pre)
    context = {"az": az, "numbertype": numbertype, "prefixes": pre, "prepost": prepost, "user_id": user_id}
    return render(request, 'dugaarShuult/dugaarShuult.html', context)


def numberPrice(request):
    logging.info("ДУГААРЫН ҮНЭ")
    number = request.GET['number']
    numbertype = request.GET['numbertype']
    az = request.GET['az']
    user_id = request.GET["user_id"]
    numbertype = Numbertype.objects.get(id=numbertype)
    logging.info(numbertype)
    aziinDugaar = AziinDugaar.objects.get(type=az)
    context = {"aziinDugaar": aziinDugaar, "numbertype": numbertype, "az": az, "number": number, "user_id": user_id}
    return render(request, 'dugaarShuult/modalNumberPrice.html', context)


def zahialga(request):
    logging.info("ДУГААРЫН ЗАХИАЛГА")
    user_id = request.GET["user_id"]
    number = request.GET['number']
    dia = request.POST['dia']
    zoriulalt = request.POST['zoriulalt']
    numbertype = request.GET['numbertype']
    logging.info(dia)
    nsn = NfilterSaveNumber()
    nsn.user_id = user_id
    nsn.numbertype = numbertype
    nsn.dia = dia
    nsn.zoriulalt = zoriulalt
    nsn.status = "A"
    nsn.numbers = number
    nsn.code = get_random_alphanumeric_string(6)
    nsn.save()
    firm_status = "0"
    if dia == "30days":

    # else:
        need_firm = NfilterNeedFirm()
        need_firm.nsn_id = nsn.id
        employee = Employee.objects.get(user_id=user_id, status='A')
        logging.info(employee.department_id)
        dpt = Department.objects.get(id=employee.department_id)
        logging.info(dpt.parent_id)
        if dpt.parent_id == 1:
            logging.info("if")
            need_firm.head_id = dpt.sign_leader_id
        else:
            logging.info("else")
            if Department.objects.get(id=dpt.parent_id).sign_leader_id == None:
                logging.info("if1")
                depart = Department.objects.get(id=dpt.parent_id).parent_id
                logging.info(depart)
                need_firm.head_id = Department.objects.get(id=depart).sign_leader_id
            else:
                logging.info("else1")
                logging.info(Department.objects.get(id=dpt.parent_id).sign_leader_id)
                need_firm.head_id = Department.objects.get(id=dpt.parent_id).sign_leader_id
            logging.info(need_firm.head_id)
        need_firm.firstfirm = "0"
        need_firm.save()
        firm_status = need_firm.firstfirm

    user_ip = get_client_ip(request)
    logging.info("user_ip: " + str(user_ip))
    # socket_results = FilternumberBlockUnblock("block", number, "", str(dia) + "#$$" + str(nsn.code))
    logging.info("firm_status")
    logging.info(firm_status)
    socket_results = FilternumberBlockUnblock("block", number, "", firm_status, str(dia), str(user_id), str(nsn.code), user_ip)
    if socket_results == "Success":
        logging.info("Хадгалсан дугаар: " + str(number))
    else:
        logging.error('Уучлаарай, таны сонгосон ' + str(number) + ' дугаар захиалах боломжгүй байна. Line-1379')
    context = {"error1": "Таны " + str(nsn.id) + " дугаартай хүсэлт амжилттай биеллээ. Код: " + str(nsn.code), "error2": "", "user_id": user_id}
    return render(request, 'dugaarShuult/timeout.html', context)


def niitDugaarShuult(request):
    logging.info("niitDugaarShuult")
    user_id = request.GET["user_id"]
    page = request.GET["page"]
    employee = Employee.objects.get(user_id=user_id)
    arr1 = []
    my = ""
    if "my" in request.GET:
        if request.GET["my"] == "":
            if NfilterNeedFirm.objects.filter(head_id=employee.id).exists():
                nnf = NfilterNeedFirm.objects.filter(head_id=employee.id)
                for i in range(len(nnf)):
                    arr1.append(NfilterSaveNumber.objects.get(id=nnf[i].nsn_id))
        else:
            logging.info("my")
            my = request.GET["my"]
            arr1 = NfilterSaveNumber.objects.filter(user_id=user_id, status='A').order_by('-id')
    else:
        logging.info("not mine")
        if NfilterNeedFirm.objects.filter(head_id=employee.id).exists():
            nnf = NfilterNeedFirm.objects.filter(head_id=employee.id)
            for i in range(len(nnf)):
                arr1.append(NfilterSaveNumber.objects.get(id=nnf[i].nsn_id))
    logging.info(arr1)

    pagination = 20
    minor = (int(page) - 1) * pagination
    if int(len(arr1) / pagination) == int(page) - 1:
        mayor = len(arr1)
    else:
        mayor = int(page) * pagination

    arr5 = []

    for i in range(minor, mayor):
        d = arr1[i].user_id
        tuluv = ""
        number_saved_date = ""
        if NfilterNeedFirm.objects.filter(nsn_id=arr1[i].id).exists():
            nfnf = NfilterNeedFirm.objects.get(nsn_id=arr1[i].id)
            tuluv = nfnf.firstfirm
            number_saved_date = nfnf.firstfirmdate

        # da = d[0]
        # if da.status == 'A':
        arr5.append({
            "id": arr1[i].id,
            "number": arr1[i].numbers,
            "zoriulalt": arr1[i].zoriulalt,
            "dia": arr1[i].dia,
            # "user": Employee.objects.get(user_id=arr1[i].user_id).name,
            "ognoo": arr1[i].created_date,
            # "tuluv": d.values(position)[0][position]
            "tuluv": tuluv,
            "number_saved_date": number_saved_date
        })
    logging.info("arr5")
    logging.info(arr5)
            # logging.info(d.values(position)[0][position])
    # logging.info("COUNT")

    # logging.info(count)

    paginator = Paginator(arr1, pagination)
    page_obj = paginator.page(page)
    logging.info(page_obj)

    context = {"user_id": user_id, "datas": arr5, "page_obj": page_obj, "my": my}
    return render(request, 'dugaarShuult/niitDugaar.html', context)


def more(request):
    logging.info("more")
    user_id = request.GET["user_id"]
    nsn_id = request.GET["nsn_id"]
    page = request.GET["page"]
    nsn = NfilterSaveNumber.objects.get(id=nsn_id)
    employee = Employee.objects.get(user_id=user_id)
    tsohoh = "yes"
    if "my" in request.GET["my"]:
        tsohoh = "no"
    if NfilterNeedFirm.objects.filter(nsn_id=nsn_id).exists():
        need_firm = NfilterNeedFirm.objects.get(nsn_id=nsn_id)
        headname = Employee.objects.get(id=need_firm.head_id).name
    else:
        need_firm = ""
        headname = ""
    saved_name = Employee.objects.get(user_id=nsn.user_id).name
    context = {"user_id": user_id, "nsn": nsn, "need_firm": need_firm, "page": page, "employee": employee, "headName": headname, "tsohoh": tsohoh, "saved_name": saved_name}
    return render(request, 'dugaarShuult/more.html', context)


def firmNumbers(request):
    logging.info("firmNumbers")
    user_id = request.GET["user_id"]
    nsn_id = request.GET["nsn_id"]
    firmado = request.POST["firmado"]
    tailbar = request.POST["tailbar"]
    employee = Employee.objects.get(user_id=user_id)
    need_firm = NfilterNeedFirm.objects.get(nsn_id=nsn_id)
    nsn = NfilterSaveNumber.objects.get(id=nsn_id)
    hariu = ""
    if firmado == "yes":
        need_firm.firstfirm = "2"
        hariu = "зөвшөөрөгдөж"
    if firmado == "no":
        need_firm.firstfirm = "3"
        hariu = "татгалзаж"

    need_firm.firstfirmdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    need_firm.firstfirmdescription = tailbar
    need_firm.save()
    logging.info(str(need_firm.nsn_id) + " " + str(firmado))
    notification = str(need_firm.nsn_id) + " дугаартай шаардах " + hariu + " амжилттай хадгалагдлаа"
    if nsn.dia == "30days":
        user_ip = get_client_ip(request)
        logging.info("user_ip: " + str(user_ip))
        socket_results = FilternumberBlockUnblock("block", nsn.numbers, "", need_firm.firstfirm, str(nsn.dia),
                                                  str(nsn.user_id), str(nsn.code), user_ip)
        if socket_results == "Success":
            logging.info("Хадгалсан дугаар: " + str(nsn.numbers))
            notification = str(need_firm.nsn_id) + " дугаартай шаардах " + hariu + " амжилттай хадгалагдлаа"
        else:
            logging.error("Уучлаарай, " + str(nsn.numbers) + " дугаарын хадгалах хугаацааг нэмж сунгаж чадсангүй. Line-1247")
            notification = "Уучлаарай, " + str(nsn.numbers) + " дугаарын хадгалах хугаацааг нэмж сунгаж чадсангүй."
    context = {"user_id": user_id, "notification": notification, "employee": employee}
    return render(request, 'notification.html', context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def FilternumberBlockUnblock(turul, number, az, firm_status, days, user_id, user_code, user_ip):
    logging.info("FilternumberBlockUnblock")
    logging.info(number)
    # logging.info("0003Block:{0}|{1}|0|{2}|0|Shaardah".format(number, "shaardah" + days + ":" + str(user.encode('utf-8')), user_ip))
    logging.info(user_ip)
    soc = socket.socket()
    soc.connect(('10.10.10.173', 8032))
    request_string = ""
    if turul == "filter":
        request_string = "0003ACC_QUERY:0|3|132|{0}|{1}".format(number, az)
    elif turul == "block":
        request_string = "0003Block:{0}|{1}|0|{2}|0|Shaardah".format(number, "shaardah" + str(firm_status) + ":" + str(days) + ":" + str(user_id) + "#" + str(user_code), user_ip)
    logging.info(request_string)
    soc.send(request_string)
    socket_results = soc.recv(2048)
    logging.info(socket_results)
    soc.close()
    return socket_results


# --------------------------FILTER NUMBER ---------------------------
# dugaar shuult

@api_view(["GET"])
def getNumber(request):
    logging.info("GETNUMBER")
    move = int(request.GET['move'])
    prefix = request.GET["prefix"]
    az = request.GET['az']
    numbertype = request.GET['numbertype']
    if numbertype == "3":
        numbertype = "2"

    first4 = prefix[0:4]
    last4 = prefix[4:8]

    res = checkLast4(last4)
    ontsgoiDugaar = "engiin"
    if az == "5":
        if last4 == "AAAA":
            ontsgoiDugaar = "alt1"
        last4 = "****"
    if az == "7":
        if last4 == "DEAB":
            ontsgoiDugaar = "mungu1"
        if last4 == "ABDE":
            ontsgoiDugaar = "mungu2"
        if last4 == "AABB":
            ontsgoiDugaar = "mungu3"
        last4 = "****"
    if az == "9":
        if last4 == "ABBA":
            ontsgoiDugaar = "hurel1"
        if last4 == "ABAB":
            ontsgoiDugaar = "hurel2"
        last4 = "****"
    if az == "6":
        if res == "alt1":
            az = "5"
            ontsgoiDugaar = "alt1"
        if res == "mungu1" or res == "mungu2" or res == "mungu3":
            az = "7"
            ontsgoiDugaar = "mungu3"
        if res == "hurel1":
            az = "9"
            ontsgoiDugaar = "hurel1"
        if res == "hurel2":
            az = "9"
            ontsgoiDugaar = "hurel2"

    prefixList = list(Prefix.objects.filter(is_active=1, prefix__contains=prefix[0:2], category=numbertype).order_by("prefix"))
    i = 0
    numbers = []

    if numbertype == "2":
        if prefix[2] == "*":
            if prefix[3] == "*":
                if res == "engiin":
                    if (prefix[4:6] != "**" and prefix[6:8] == "**") or (prefix[4] == "*" and prefix[5:7] != "**" and prefix[7] == "*") or (prefix[4] != "*" and prefix[5:7] == "**" and prefix[7] != "*") \
                            or (prefix[4:6] == "**" and prefix[6:8] != "**") or (prefix[4] != "*" and prefix[5] == "*" and prefix[6] != "*" and prefix[7] == "*") \
                            or (prefix[4] == "*" and prefix[5] != "*" and prefix[6] == "*" and prefix[7] != "*") or (prefix[2:8] == "******"):
                        first4 = str(prefixList[i].prefix)
                    else:
                        first4 = first4
                else:
                    if ontsgoiDugaar != "engiin":
                        if az == "7" or az == "9":
                            first4 = str(prefixList[i].prefix)
            else:
                digit4 = []
                for j in range(0, len(prefixList)):
                    if str(prefixList[j].prefix)[3] == prefix[3]:
                        digit4.append(prefixList[j].prefix)
                first4 = str(digit4[i])
        if prefix[2] == "1" and prefix[3] == "*":
            first4 = str(prefixList[i].prefix)

    start = first4 + last4
    prefix = ''.join(str(k) for k in start)

    # socket_results = FilternumberBlockUnblock("filter", prefix, az, "")
    socket_results = FilternumberBlockUnblock("filter", prefix, az, "", "", "", "", "")
    if socket_results != "-1":
        socket_results = socket_results.split('|')
    else:
        socket_results = None
    if socket_results != None:
        for number in socket_results:
            data = number.split(":")
            if data[1] == az:
                numbers.append(data[0])

    tmp = []
    i = 0
    while (i < len(numbers)):
        numero = numbers[i]
        numero = numero[0:4]
        if Prefix.objects.filter(is_active=1, prefix__contains=numero, category=numbertype).exists() and numero != "9811":
            tmp.append(numbers[i])
        i += 1
    numbers = tmp

    if 'movedown' in request.GET:
        # if socket_results != None:
        if len(numbers) > move + 24:
            numbers = numbers[move:move + 24]
            move = move + 24
        elif len(numbers) - move > 0:
            numbers = numbers[move:len(numbers)]
            move = move + 24
        elif len(numbers) == 0:
            move = 24
            numbers = None
        else:
            move = len(numbers) - 24
            # else:
            #   numbers = None
    else:
        # if socket_results != None:
        if len(numbers) != 0:
            if move > 24:
                numbers = numbers[move - 24:move + 23]
                move = move - 24
            elif move <= 24:
                numbers = numbers[0:24]
                move = 24
        else:
            numbers = None
            move = 24
            # else:
            #   numbers = None

    result = []
    data_number = dict()
    if numbers != None:
        for number in numbers:
            if checkNumber(number) == ontsgoiDugaar:
                data_number[str(number)] = number
    result.append(data_number)
    result.append(move)
    result.append(res)

    return Response(result)

def checkNumber(number):
    oron1 = number[0:1]
    oron2 = number[1:2]
    oron3 = number[2:3]
    oron4 = number[3:4]
    oron5 = number[4:5]
    oron6 = number[5:6]
    oron7 = number[6:7]
    oron8 = number[7:8]

    # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
    if (((oron3 != oron4) and (oron4 != oron5) and (oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)) or (
                        (oron3 != oron4) and (oron3 == oron5) and (oron4 != oron5) and (oron5 == oron6) and (
            oron6 == oron7) and (oron7 == oron8)) or (
                    (oron3 != oron4) and (oron4 == oron5) and (oron5 == oron6) and (oron6 == oron7) and (
        oron7 == oron8))):
        return "alt1"

    # silver shalgah DEABABDE, DExxAABB, DEABDEAB
    # DEABDEAB
    if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
        return "mungu1"
    # DEABABDE
    if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
        return "mungu2"
    # DExxAABB
    if (((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)) or (
                    (oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7) and (oron2 != oron5) and (
        oron2 != oron7))):
        return "mungu3"
    # hurel shalgah DExxABBA, DExxABAB
    # DExxABBA
    if ((oron1 != oron2) and (oron5 == oron8) and (oron6 == oron7)):
        return "hurel1"
    # DExxABAB
    if ((oron5 == oron7) and (oron6 == oron8)):
        return "hurel2"
    else:
        return "engiin"


def checkLast4(last4):
    oron5 = last4[0:1]
    oron6 = last4[1:2]
    oron7 = last4[2:3]
    oron8 = last4[3:4]

    if oron5 != "*" and oron6 != "*" and oron7 != "*" and oron8 != "*": # last4 != "****"
        # golden shalgah DEABCCCC, DECBCCCC, DEACCCCC
        if ((oron5 == oron6) and (oron6 == oron7) and (oron7 == oron8)):
            return "alt1"
        # silver shalgah DEABABDE, DExxAABB, DEABDEAB
        # DEABDEAB
        # if ((oron1 == oron5) and (oron2 == oron6) and (oron3 == oron7) and (oron4 == oron8)):
        #     return "mungu1"
        # # DEABABDE
        # if ((oron1 == oron7) and (oron2 == oron8) and (oron3 == oron5) and (oron4 == oron6) and (oron3 != oron4)):
        #     return "mungu2"
        # DExxAABB
        if ((oron5 == oron6) and (oron7 == oron8) and (oron6 != oron7)):
            return "mungu3"

        # hurel shalgah DExxABBA, DExxABAB
        # DExxABBA
        if ((oron5 == oron8) and (oron6 == oron7)):
            return "hurel1"
        # DExxABAB
        if ((oron5 == oron7) and (oron6 == oron8)):
            return "hurel2"
        else:
            return "engiin"
    else:
        return "engiin"
