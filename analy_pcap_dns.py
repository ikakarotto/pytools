#!/usr/bin/env python3
# coding: utf-8
import os
import subprocess
import re
import sys
import platform
import geoip2.database

def ip2location(ipaddr):
    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ipaddr)
        area = response.country.iso_code
        return area
    except geoip2.errors.AddressNotFoundError:
        # print("ipaddr(%s) can not found in geoip2 database" % ipaddr)
        # pass
        return "NotFound"

def bytes2str(bytedata):
    if platform.system() == "Windows":
        return bytedata.decode('gbk','ignore')
    elif platform.system() == "Linux":
        return str(bytedata, encoding = "utf-8")

def win_analy_pcap_dns(filedir, filename):
    cmdline = "cd %s && windump -nnvvv -XX -r %s udp and src port 53" % (filedir, filename)
    pattern_domain = re.compile(r'.* q: A\? (.*?). .*')
    pattern_answer = re.compile(r'.*?( A .*)')
    data = subprocess.run(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    for line in data.stdout.decode('gbk','ignore').split('\r\n'):
        if re.search('\d+ q: A\? ',line):
            reobj_hostname = pattern_domain.match(line)
            if reobj_hostname:
                query_hostname = reobj_hostname.groups()[0]
                answer = pattern_answer.match(line).groups()[0]
                records = re.findall(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',answer)
                # print(query_hostname, records)
                print(query_hostname, end="")
                for record in records: print("," + record + "(" + ip2location(record) + ")", end="")
            print()

def linux_analy_pcap_dns(filedir, filename):
    cmdline = "cd %s && tcpdump -nnvvv -XX -r %s udp and port 53" % (filedir, filename)
    pattern_domain = re.compile(r'.* q: A\? (.*?). .*')
    pattern_answer = re.compile(r'.*?( A .*)')
    data = subprocess.run(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    for line in str(data.stdout, encoding = "utf-8").split('\n'):
        if re.search('\d+ q: A\? ',line):
            reobj_hostname = pattern_domain.match(line)
            if reobj_hostname:
                query_hostname = reobj_hostname.groups()[0]
                answer = pattern_answer.match(line).groups()[0]
                records = re.findall(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',answer)
                # print(query_hostname, records)
                print(query_hostname, end="")
                #for record in records: print("\t" + record, end="")
                for record in records: print("," + record + "(" + ip2location(record) + ")", end="")
            print()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please enter a pcap file!!!")
        sys.exit(1)
    else:
        filepath = sys.argv[1]

    if os.path.isfile(filepath):
        filedir = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        if not filedir: filedir = os.getcwd()
        if platform.system() == "Windows":
            cmdline = 'where windump'
            checkcmd = subprocess.run(cmdline,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            if not checkcmd.returncode:
                win_analy_pcap_dns(filedir, filename)
            else:
                print("[%s] %s" % (cmdline, checkcmd.stderr.decode('gbk','ignore').strip()))

        elif platform.system() == "Linux":
            cmdline = 'which tcpdump'
            checkcmd = subprocess.run(cmdline,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            if not checkcmd.returncode:
                linux_analy_pcap_dns(filedir, filename)
            else:
                print("[%s] %s" % (cmdline, checkcmd.stderr.strip()))
        else:
            print("Platform unknown.")

    else:
        print("No such file: [%s]" % filepath)


# python3 analy_pcap_dns.py ios-pay.pcap
