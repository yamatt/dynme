#!/usr/bin/env python3

import argparse
import logging

import requests
from lxml import etree

URL = "https://www.namesilo.com/api/dnsListRecords?version=1" \
      "&type={type}&key={key}&domain={domain}"

def url(key, domain, type="xml"):
    return URL.format(
        type=type,
        key=key,
        domain=domain
    )

def get_result(url):
    return requests.get(url).text
    
def get_xml(url):
    return etree.fromstring(get_result(url))
    
def xml_ok(x):
    return x.xpath("/namesilo/reply/code")[0].text == "300"
    
def render_xml(x):
    for record in x.xpath("/namesilo/reply/resource_record"):
        print("\t".join([
            record.xpath("host")[0].text,
            record.xpath("type")[0].text,
            record.xpath("ttl")[0].text,
            record.xpath("record_id")[0].text
        ]))
    
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
    
    parser.add_argument('domain',
        help='Domain name to check'
    )
    
    args = parser.parse_args()
    
    logging.basicConfig(level=args.loglevel)

    return args

if __name__ == "__main__":
    args = get_args()
    url = URL.format(
        type="xml",
        key=args.key,
        domain=args.domain
    )
    logging.info("Accessing URL: {url}".format(url=url))
    xml = get_xml(url)
    if not xml_ok(xml):
        logging.error(
            "There was an error accessing the API: {0}".format(
                xml.xpath("/namesilo/reply/detail")[0].text
            )
        )
    render_xml(xml)
        
