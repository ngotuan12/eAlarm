'''
Created on Aug 28, 2014

@author: TuanNA
'''
import json

import requests
from eAlarmWebapp import settings

def getAuthorization():
    url = settings.ALARM_SERVER + settings.PERMISSION_SERVICE
    payload = {"Method":"login","UserName":"TuanNA","PassWord":"113322"}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":""}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    print(response['Authorization'])
    return response['Authorization']

def exportDeviceReport(authorization,device_id,area_id,device_status):
    url = settings.ALARM_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"DeviceReport","device_id":device_id,"area_id":area_id,"device_status":device_status}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportDeviceDetailReport(authorization,device_id,area_id,device_status,from_date,to_date):
    url = settings.ALARM_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"DeviceDetailReport",
               "device_id":device_id,
               "area_id":area_id,
               "device_status":device_status,
               "from_date":from_date,
               "to_date":to_date,}
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportDeviceErrorReport(authorization,device_id,area_id,device_status,property_id,from_date,to_date):
    url = settings.ALARM_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"DeviceErrorReport",
               "device_id":device_id,
               "area_id":area_id,
               "device_status":device_status,
               "property_id":property_id,
               "from_date":from_date,
               "to_date":to_date,
               }
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout
def exportSensorMirrorReport(authorization,device_id,area_id,device_status,property_id,from_date,to_date):
    url = settings.ALARM_SERVER + settings.REPORT_SERVICE
    payload = {"SessionUserName":"TuanNA","Method":"SensorMirrorReport",
               "device_id":device_id,
               "area_id":area_id,
               "device_status":device_status,
               "property_id":property_id,
               "from_date":from_date,
               "to_date":to_date,
               }
    headers = {'content-type': 'application/json;charset=utf-8',"Authorization":authorization}
    r = requests.request('POST',url, data=json.dumps(payload), headers=headers)
    response = r.json()
    fileout = response['FileOut']
    return fileout