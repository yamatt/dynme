#!/usr/bin/env python3

import argparse
import logging

import requests
from lxml import etree

URL = "https://www.namesilo.com/api/dnsUpdateRecord?version=1" \
        "&type={type}" \
        "&key={key}" \
        "&domain={domain}" \
        "&rrid={id}" \
        "&rrhost={subdomain}" \
        "&rrvalue={ip}" \
        "&rrttl={ttl}"

def url(key, domain, id, subdomain, value, type="xml", ttl=""):
    return URL.format(
        type=type,
        key=key,
        domain=domain,
        id=id,
        subdomain=subdomain,
        value=value,
        ttl=ttl
    )

def get_result(url):
    return requests.get(url).text
    
def get_xml(url):
    return etree.fromstring(get_result(url))
    
def get_args():
    parser = argparse.ArgumentParser(
        description='Find domains in DNS'
    )
    parser.add_argument('-k', '--key', required=True,
        help='Key for API access'
    )
    parser.add_argument("-l", "--log-level", 
        dest="loglevel",
        default='WARNING',
        help='Set the logging output level.'
    )
    
    parser.add_argument('-d', '--domain', required=True,
        help='Domain name to update'
    )
    parser.add_argument('-i', '--id', required=True,
        help='Record ID'
    )
    parser.add_argument('-s', '--subdomain', required=True,
        help='Subdomain name to update'
    )
    parser.add_argument('-p', '--ip', required=True,
        help='IP value to update the entry to'
    )
    parser.add_argument('-t', '--ttl', default="",
        help='IP value to update the entry to'
    )
    
    args = parser.parse_args()
    
    logging.basicConfig(level=args.loglevel)

    return args

if __name__ == "__main__":
    args = get_args()
    url = URL.format(
        type="xml",
        key=args.key,
        domain=args.domain,
        id=args.id,
        subdomain=args.subdomain,
        ip=args.ip,
        ttl=args.ttl
    )
    logging.info("Accessing URL: {url}".format(url=url))
    xml = get_xml(url)
    print(etree.tostring(xml, pretty_print=True))
