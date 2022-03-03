#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : get_kernels.py
# Author             : Podalirius (@podalirius_)
# Date created       : 3 Mar 2022

# https://cdn.kernel.org/pub/linux/kernel/

import json
import os
import re
import requests
from bs4 import BeautifulSoup

## List versions
r = requests.get('https://cdn.kernel.org/pub/linux/kernel/')
versions = [a['href'] for a in BeautifulSoup(r.content.decode('UTF-8'), 'lxml').findAll('a') if a['href'].startswith('v')]

listofkernels = {'kernels': {}}
for version in versions:
    print('[+] Parsing %s ...' % version)
    r = requests.get('https://cdn.kernel.org/pub/linux/kernel/%s/' % version)
    soup = BeautifulSoup(r.content.decode('UTF-8'), 'lxml')
    for a in soup.findAll('a'):
        if a['href'].startswith('linux'):
            kernel = {}
            filename = os.path.basename(a['href']).replace('linux-', '')

            kernel['link'] = 'https://cdn.kernel.org/pub/linux/kernel/%s%s' % (version, a['href'])
            version = '.'.join(filename.split('.')[:-1])
            if version.endswith(".tar"):
                version = '.'.join(filename.split('.')[:-1])
            kernel['version'] = version
            kernel['major'] = kernel['version'].split('.')[0]
            kernel['minor'] = kernel['version'].split('.')[1]

            if kernel['major'] not in listofkernels['kernels'].keys():
                listofkernels['kernels'][kernel['major']] = {}

            if kernel['minor'] not in listofkernels['kernels'][kernel['major']].keys():
                listofkernels['kernels'][kernel['major']][kernel['minor']] = []

            listofkernels['kernels'][kernel['major']][kernel['minor']].append(kernel)

f = open('kernels.json', 'w')
f.write(json.dumps(listofkernels, indent=4))
f.close()
