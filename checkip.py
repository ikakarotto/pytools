#!/usr/bin/env python3
# coding: utf-8
import sys
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
    if len(sys.argv) != 2:
        print("Please enter a pcap file!!!")
        sys.exit(1)
    else:
        ipaddr = sys.argv[1]

    country = ip2country(ipaddr)
    city = ip2city(ipaddr)
    (aso,asn,prefix_len) = ip2asn(ipaddr)
    result = "%s\t%s\t%s\t%s\t%s" % (country,city,aso,asn,prefix_len)
    print(result)
