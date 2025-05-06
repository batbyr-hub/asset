# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

# import serializers
from .models import *
from datetime import datetime
import logging
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework import status
from myapi.serializers import DataSerializer

log_date = datetime.now().strftime('%Y-%m-%d')
# log_file = 'Logs/Log_{0}'.format(log_date)
log_file = 'home/bam/asset/Logs/Log_{0}'.format(log_date)
logging.basicConfig(filename=log_file + '.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

@api_view(['GET', 'POST', 'DELETE'])
def saveDataAsset(request):
    logging.info("saveDataAsset")
    if request.method == 'GET':
        logging.info("GET")
        response = {
            "status": "unsuccessful",
            "message": "NOT allowed method"
        }
        return JsonResponse(response, safe=False)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        logging.info("POST")
        asset_data = JSONParser().parse(request)
        if AssetPackageData.objects.filter(assetslipid=asset_data["assetslipid"]).exists():
            detailsData = AssetDetailsData()
            detailsData.assetslipid = asset_data["assetslipid"]
            detailsData.assetgroupname = asset_data["assetgroupname"]
            detailsData.assetname = asset_data["assetname"]
            detailsData.assetbarcode = asset_data["assetbarcode"]
            detailsData.returnis = asset_data["returnis"]
            detailsData.seleccion = asset_data["seleccion"]
            detailsData.lenghtcable = asset_data["lenghtcable"]
            detailsData.status = asset_data["status"]
            detailsData.save()
        else:
            packageData = AssetPackageData()
            packageData.assetslipid = asset_data["assetslipid"]
            packageData.locationfrom = asset_data["locationfrom"]
            packageData.locationto = asset_data["locationto"]
            packageData.createddate = asset_data["createddate"]
            packageData.location_id = asset_data["location_id"]
            packageData.locationfrom_id = asset_data["locationfrom_id"]
            packageData.userfrom = asset_data["userfrom"]
            packageData.userto = asset_data["userto"]
            packageData.gazar = asset_data["gazar"]
            packageData.reasonvalue = asset_data["reasonvalue"]
            packageData.uploadfile = asset_data["uploadfile"]
            packageData.status = asset_data["status"]
            packageData.save()

            detailsData = AssetDetailsData()
            detailsData.assetslipid = asset_data["assetslipid"]
            detailsData.assetgroupname = asset_data["assetgroupname"]
            detailsData.assetname = asset_data["assetname"]
            detailsData.assetbarcode = asset_data["assetbarcode"]
            detailsData.returnis = asset_data["returnis"]
            detailsData.seleccion = asset_data["seleccion"]
            detailsData.lenghtcable = asset_data["lenghtcable"]
            detailsData.status = asset_data["status"]
            detailsData.save()

            permission = AssetPermission.objects.filter(status='A').order_by('level')
            logging.info("permission")
            logging.info(len(permission))
            for i in range(len(permission)):
                firmData = AssetFirmData()
                firmData.assetpackagedataid = packageData.id
                firmData.userid = permission[i].id
                firmData.status = "0"
                firmData.save()

        response = {
            "status": "successful",
            "message": "Registered"
        }
        logging.info(asset_data["assetslipid"])
        logging.info(response)
        return JsonResponse(response, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        logging.info("DELETE")
        # count = Data.objects.all().delete()
        # return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])},
        #                     status=status.HTTP_204_NO_CONTENT)
        asset_data = JSONParser().parse(request)
        if AssetPackageData.objects.filter(assetslipid=asset_data["assetslipid"]).exists():
            asset_package_data = AssetPackageData.objects.get(assetslipid=asset_data["assetslipid"])
            asset_package_data.status = "D"
            asset_package_data.save()
            response = {
                "status": "successful",
                "message": "Deleted"
            }
            logging.info(asset_data["assetslipid"])
            logging.info(response)
            return JsonResponse(response, status=status.HTTP_200_OK)
        else:
            response = {
                "status": "unsuccessful",
                "message": "Not deleted"
            }
            logging.info(asset_data["assetslipid"])
            logging.info(response)
            return JsonResponse(response, status=status.HTTP_200_OK)

# def deleteAssetslipid(request):
#     logging.info("saveDataAsset")
#     if request.method == 'GET':
#         logging.info("GET")
#         response = {
#             "status": "unsuccessful",
#             "message": "NOT allowed method"
#         }
#         return JsonResponse(response, safe=False)
#         # 'safe=False' for objects serialization
#
#     elif request.method == 'POST':
#         logging.info("POST")
#         asset_data = JSONParser().parse(request)
#         if AssetPackageData.objects.filter(assetslipid=asset_data["assetslipid"]).exists():
#             detailsData = AssetDetailsData()
