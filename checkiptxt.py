#!/usr/bin/env python3
# coding: utf-8
from os.path import basename
from sys import argv
import geoip2.database

def ip2country(ipaddr):
    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ipaddr)
        area = response.country.iso_code
        return area
    except (ValueError,geoip2.errors.AddressNotFoundError):
        # print("ipaddr(%s) can not found in geoip2 database" % ipaddr)
        # pass
        return "NotFound"

def ip2city(ipaddr):
    try:
        reader = geoip2.database.Reader('GeoLite2-City.mmdb')
        response = reader.city(ipaddr)
        if response.subdivisions: 
            #print(response.subdivisions[0])
            #area = response.subdivisions[0].names['zh-CN']
            try:
                area = response.city.names['en']
            except:
                area = response.subdivisions[0].names['en']
            return area

    except (ValueError,geoip2.errors.AddressNotFoundError):
        # print("ipaddr(%s) can not found in geoip2 database" % ipaddr)
        # pass
        return "NotFound"

def ip2asn(ipaddr):
    try:
        reader = geoip2.database.Reader('GeoLite2-ASN.mmdb')
        response = reader.asn(ipaddr)
        #print(response)
        aso = response.autonomous_system_organization.replace("Data Communication Business Group","Data Communication Business Group (HINET)").replace("Mobile Business Group","Mobile Business Group (HINET)")
        asn = response.raw.get('autonomous_system_number')
        prefix_len = response.raw.get('prefix_len')
        return aso,asn,prefix_len
    except (ValueError,geoip2.errors.AddressNotFoundError):
        # print("ipaddr(%s) can not found in geoip2 database" % ipaddr)
        # pass
        return ("NotFound","NotFound","NotFound")

if __name__ == '__main__':
    '''
    if len(sys.argv) != 2:
        print("Please enter a pcap file!!!")
        sys.exit(1)
    else:
        ipaddr = sys.argv[1]
    '''

    infile = argv[1]
    outfile = basename(infile).split('.')[0] + '-reverse.txt'
    fdout = open(outfile, 'a+', encoding="utf-8")

    with open(infile,'r') as fd:
        for ipaddr in fd.readlines():
            ipaddr = ipaddr.strip()
            country = city = aso = asn = 'NotFound'
            #print(ip2country(ipaddr))
            #print(ip2city(ipaddr))
            #print(ip2asn(ipaddr))

            country = ip2country(ipaddr)
            city = ip2city(ipaddr)
            (aso,asn,prefix_len) = ip2asn(ipaddr)
            #result = "%s\t%s\t%s" % (country,city,asn)
            result = "%s\t%s\t%s\t%s\t%s\t%s" % (ipaddr,country,city,aso,asn,prefix_len)
            print(result)
            fdout.write(result + '\n')
    fdout.close()

