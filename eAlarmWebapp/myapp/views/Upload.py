'''
Created on Dec 3, 2014

@author: TuanNA
'''
import os

from eAlarmWebapp.settings import STATIC_ROOT


def handle_uploaded_file(upload_type,f):
    folder_path = STATIC_ROOT+"/upload/"+upload_type+"/";
    url = "/upload/"+upload_type+"/" + f.name
    if os.path.isdir(folder_path) == False:
        os.makedirs(folder_path)
    with open(folder_path+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)