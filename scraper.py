#!/usr/bin/env python

import datetime
import requests
from lxml import etree


DMV_OFFICES_URL = "http://apps.dmv.ca.gov/fo/offices/appl/fo_data/foims_XmlFOdata.xml"
DMV_DATA_URL = "http://apps.dmv.ca.gov/fo/offices/apps/foGeoXml_v2.jsp?foNumb="


def get_office_data():
    '''Downloads information for all the CA DMV offices and saves it'''
    r = requests.get(DMV_OFFICES_URL)
    if r.status_code == 200:
        print(r.text)


def parse_office(data):
    '''Takes part of an XML tree and returns an office object'''
    pass


def get_all_wait_data():
    '''Downloads wait time data for every DMV office the script knows about'''
    pass


def get_office_wait_data(office, time=datetime.datetime.now()):
    '''Gets the current wait time for a given DMV office'''
    pass


def parse_current_wait_time(data):
    '''Parses a given wait time'''
    pass