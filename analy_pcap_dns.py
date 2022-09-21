#!/usr/bin/env python3
# coding: utf-8
# mdate: 20220921
import os
import subprocess
import re
import sys
import platform
import geoip2.database

# 字符串转码
def bytes2str(bytedata):
    if platform.system() == "Windows":
        return bytedata.decode('gbk','ignore')
    elif platform.system() == "Linux":
        return str(bytedata, encoding = "utf-8")

# 查询country code
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

# 根据DNS查询获取IP和域名的映射关系
def analy_pcap_dns_from_answer(filedir, filename, cmd, linesep):
    cmdline = "cd %s && %s -nnvvv -XX -r %s udp and port 53" % (filedir, cmd, filename)
    pattern_domain = re.compile(r'.* q: A\? (.*?). .*')
    pattern_answer = re.compile(r'.*?( A .*)')
    data = subprocess.run(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    allrecords = []
    for line in bytes2str(data.stdout).split(linesep):
        if re.search('\d+ q: A\? ',line):
            reobj_hostname = pattern_domain.match(line)
            if reobj_hostname:
                query_hostname = reobj_hostname.groups()[0]
                answer = pattern_answer.match(line).groups()[0]
                records = re.findall(r'(?:(?:25[0-5]|2[0-4]\d|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)',answer)
                for record in records:
                    allrecords.append((record, query_hostname, ip2location(record)))
    return allrecords

# 从字符串中匹配IP地址
def parse_ipaddr(s):
    if re.search(r'.* > (.*?): .*',s):
        ip_port = re.search(r'.* > (.*?): .*',s).groups()[0]
        ip = '.'.join(ip_port.split('.')[:4])
        return ip

# 从16进制的字符串中匹配域名
def parse_domain(b):
    ascii_text = bytearray.fromhex(b).decode('latin-1')
    reobj_host = re.compile('(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?')
    for domain in reobj_host.findall(ascii_text, re.S):
        if not re.search('^\d+\.\d+$', domain):
            if re.search('^(([a-zA-Z0-9-]+\.)+[a-zA-Z0-9]+)$', domain):
                return domain

# 从tls握手包中获取IP和域名的映射关系
def analy_pcap_dns_from_tls_client_hello(filedir, filename, cmd, linesep):
    cmdline = "cd %s && %s -nn -xx -r %s \"(tcp[((tcp[12] & 0xf0) >>2)] = 0x16)  && (tcp[((tcp[12] & 0xf0) >>2)+5] = 0x01)\"" % (filedir, cmd, filename)
    data = subprocess.run(cmdline,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if data.returncode: print(bytes2str(data.stderr).strip())

    frames = bytes2str(data.stdout).split(linesep)
    frames = [frame.replace('0x0000','separate 0x0000') for frame in frames]
    frames = [re.sub(r'\d{2}:\d{2}:\d{2}\.\d+','a_new_frame:', frame) for frame in frames]
    allstrings = ''
    for i in frames:
        if re.search(r'0x\w{4}:', i):
            i = re.sub(r'0x\w{4}:','',i)
        allstrings+=i
    frames_list = allstrings.split('a_new_frame: ')
    allrecords = []
    for i in frames_list:
        try:
            frame_info, frame_hex = i.split('separate')
            ipaddr = parse_ipaddr(frame_info)
            domain = parse_domain(frame_hex)
            if ipaddr and domain:
                #print(ipaddr,domain,ip2location(ipaddr))
                allrecords.append((ipaddr,domain,ip2location(ipaddr)))
        except Exception as err:
            #raise err
            pass
    return allrecords

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
        try:
            if platform.system() == "Windows":
                linesep = '\r\n'
                cmd = 'windump'
                cmdline = 'where %s' % cmd
            elif platform.system() == "Linux":
                linesep = '\n'
                cmd = 'tcpdump'
                cmdline = 'which %s' % cmd
            checkcmd = subprocess.run(cmdline,shell=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
            if not checkcmd.returncode:
                allrecords1 = analy_pcap_dns_from_tls_client_hello(filedir, filename, cmd, linesep)
                allrecords2 = analy_pcap_dns_from_answer(filedir, filename, cmd, linesep)
                allrecords = list(set(allrecords1 + allrecords2))
                for record in allrecords:
                    #print(record)
                    data = """'%s','%s','%s'""" % record
                    print(data)
            else:
                print("[%s] %s" % (cmdline, bytes2str(checkcmd.stderr).strip()))

        except Exception as err:
            raise err

    else:
        print("No such file: [%s]" % filepath)



# python3 analy_pcap_dns.py ios-pay.pcap
