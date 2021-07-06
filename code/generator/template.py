'''
Author: Lee Chun Hao
GitHub: https://github.com/0x4F776C
LinkedIn: https://sg.linkedin.com/in/lee-chun-hao
'''

import requests
import base64
import string
import uuid
import random
import time
from scapy.all import *

global dst_ip
dst_ip = "200.200.200.200"

def createFlag():
    generate_flag = str(uuid.uuid4())
    flag_unsterilized = base64.b64encode(bytes(generate_flag, 'utf-8'))
    flag = flag_unsterilized.decode('utf-8')
    return flag

def createDomain():
    letters = string.ascii_lowercase
    length = random.randint(8, 24)
    domain = ''.join(random.choice(letters) for i in range(length))
    return domain

def createRubbish():
    chars = string.ascii_lowercase
    length = random.randint(64, 65535)
    data = ''.join(random.choice(chars) for i in range(length))
    return data

def randomSize():
    size = random.randint(1000, 65535)
    return size

def fuzzDataTCP():
    src_ip = RandIP()._fix()
    # dst_ip = RandIP()._fix()
    packet = IP(src=src_ip, dst=dst_ip) / fuzz(TCP()) / Raw(RandString(size=randomSize()))
    return send(packet)

def fuzzDataHTTP():
    rick_roll = "aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUXc0dzlXZ1hjUSZhYl9jaGFubmVsPVJpY2tBc3RsZXlWRVZP"
    host_troll, ua_troll, data_troll = rick_roll, rick_roll, rick_roll
    host = RandIP()._fix()
    ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    data = createRubbish()
    selection = random.randint(0, 2)
    if selection == 0:
        headers = {
            'Host': host_troll,
            'User-Agent': ua,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/', headers=headers, data=data, verify=False)
        return response
    elif selection == 1:
        headers = {
            'Host': host,
            'User-Agent': ua_troll,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/', headers=headers, data=data, verify=False)
        return response
    elif selection == 2:
        headers = {
            'Host': host,
            'User-Agent': ua,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/', headers=headers, data=data_troll, verify=False)
        return response
    else:
        return "Unknown error encountered"

def fuzzDataICMP():
    src_ip = RandIP()._fix()
    # dst_ip = RandIP()._fix()
    data = createRubbish()
    packet = IP(src=src_ip, dst=dst_ip) / ICMP() / data
    return(send(packet))

def fuzzDataDNS():
    src_ip = RandIP()._fix()
    # dst_ip = RandIP()._fix()
    data = createRubbish()
    packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=random.randint(1025, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname=data))
    return send(packet)

def addFlagToDB(flag_content):
    finalised_flag = "%s" % flag_content
    headers = {
        'Host': 'localhost:8888',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://localhost:8888',
        'Connection': 'close',
        'Referer': 'http://localhost:8888/',
        'Upgrade-Insecure-Requests': '1',
    }
    data = 'flag=%s' % finalised_flag
    response = requests.post('http://localhost:8888/insert', headers=headers, data=data, verify=False)
    return response

def tcpTraffic(flag_content):
    src_ip = RandIP()._fix()
    # dst_ip = RandIP()._fix()
    flag = "flag{%s}" % flag_content
    packet = IP(src=src_ip, dst=dst_ip) / fuzz(TCP()) / Raw(load=flag)
    return send(packet)

def httpTraffic(flag_content):
    host_flag, ua_flag, url_flag, data_flag = "flag{%s}" % flag_content, "flag{%s}" % flag_content, "flag{%s}" % flag_content, "flag{%s}" % flag_content
    host = RandIP()._fix()
    ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    data = createRubbish()
    selection = random.randint(0, 3)
    if selection == 0:
        headers = {
            'Host': host_flag,
            'User-Agent': ua,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/', headers=headers, data=data, verify=False)
        return response
    elif selection == 1:
        headers = {
            'Host': host,
            'User-Agent': ua_flag,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/', headers=headers, data=data, verify=False)
        return response
    elif selection == 2:
        headers = {
            'Host': host,
            'User-Agent': ua,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/' + url_flag, headers=headers, data=data, verify=False)
        return response
    elif selection == 3:
        headers = {
            'Host': host,
            'User-Agent': ua,
            'Accept-Encoding': 'gzip deflate',
            'Accept': '*/*',
        }
        response = requests.post('http://' + dst_ip + '/', headers=headers, data=data_flag, verify=False)
        return response
    else:
        return "Unknown error encountered"

def icmpTraffic(flag_content):
    src_ip = RandIP()._fix()
    # dst_ip = RandIP()._fix()
    flag = "flag{%s}" % flag_content
    packet = IP(src=src_ip, dst=dst_ip) / ICMP() / flag
    return(send(packet))

def dnsTraffic(flag_content):
    src_ip = RandIP()._fix()
    # dst_ip = RandIP()._fix()
    flag = "flag{%s}" % flag_content
    packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=random.randint(1025, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname=flag))
    return send(packet)

def sleepTimer():
    time.sleep(random.randint(1, 2))
