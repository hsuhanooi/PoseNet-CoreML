#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import json
import os
import yaml
import requests

f = open("config.yaml", "r+")
cfg = yaml.load(f)
GOOGLE_CLOUD_STORAGE_DIR = cfg['GOOGLE_CLOUD_STORAGE_DIR']
checkpoints = cfg['checkpoints']
chk = cfg['chk']

def download(chkpoint,filename):

    url = os.path.join(GOOGLE_CLOUD_STORAGE_DIR , chkpoint , filename)
    filestore = os.path.join('./waits/' , chkpoint, filename)

    res = requests.get(url)
    if res.status_code == 200:
        if filename == 'manifest.json':
            with open(filestore, 'w') as fp:
                fp.write(res.text)
        else:
            with open(filestore, 'wb') as fp:
                fp.write(res.content)

if __name__ == "__main__":

    chkpoint = checkpoints[chk]
    print(chkpoint)
    save_dir = './waits/'+ chkpoint
    print(save_dir)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    download(chkpoint, 'manifest.json')

    f = open(os.path.join(save_dir,'manifest.json'), 'r')
    json_dict = json.load(f)

    for x in json_dict:
        filename = json_dict[x]['filename']
        print(filename)
        download(chkpoint,filename)
