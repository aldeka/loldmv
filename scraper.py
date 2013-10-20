#!/usr/bin/env python

import requests
from lxml import etree


DMV_OFFICES_URL = "http://apps.dmv.ca.gov/fo/offices/appl/fo_data/foims_XmlFOdata.xml"
DMV_DATA_URL = "http://apps.dmv.ca.gov/fo/offices/apps/foGeoXml_v2.jsp?foNumb="


def get_office_data():
    r = requests.get(DMV_OFFICES_URL)
    if r.status_code == 200:
        print(r.text)