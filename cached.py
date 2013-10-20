#!/usr/bin/env python
import os
# import subprocess
import requests
from lxml import etree


DMV_OFFICES_URL = "http://apps.dmv.ca.gov/fo/offices/appl/fo_data/foims_XmlFOdata.xml"
DMV_DATA_URL = "http://apps.dmv.ca.gov/fo/offices/apps/foGeoXml_v2.jsp?foNumb="

def download_offices(refresh=False):
  '''Download office ID data'''
  outfile = "offices.xml"
  try:
    os.stat(outfile)
    print 'Using cached copy of', outfile
  except OSError:
    refresh = True
  if refresh:
    # subprocess.check_call(['curl', '-o', outfile, 'http://apps.dmv.ca.gov/fo/offices/appl/fo_data/foims_XmlFOdata.xml'])
    r = requests.get(DMV_OFFICES_URL)
    assert r.status_code == 200, "HTTP error %s" % (r.status_code,)
    fout = open(outfile, 'w')
    for line in r.text:
      fout.write(line)

def parse_office_nums():
  '''Returns a list of the valid ID numbers for DMV offices'''
  foims = open('offices.xml','rb')
  tree = etree.parse(foims)
  foims.close()
  root = tree.getroot()
  results = []
  children = root.iter()
  first = children.next()
  assert first.tag == 'offices', "Ugh, the offices structure has changed!"
  for child in children:
    assert child.tag == 'fo_office', 'Bad child. %s' % (child,)
    results.append(int(child.attrib['num'],10))
  return results

def get_wait_time(office_id, refresh=True):
  '''Downloads data for a given office ID number and returns the wait time'''
  r = requests.get(DMV_OFFICES_URL + str(office_id))
  assert r.status_code == 200, "HTTP error %s" % (r.status_code,)
  return parse_wait(r.text)

def parse_wait(data):
  '''Returns the non-appointment wait time in minutes'''
  tree = etree.parse(data)
  root = tree.getroot()
  hour, mins = root.find('./fo_office/nonAppt').text.split(':')
  return int(hour,10) * 60 + int(mins,10)


if __name__ == "__main__":
  download_offices()
  valid_nums = parse_office_nums()
  assert len(valid_nums) == len(set(valid_nums)), "Some office indices repeat!"
  print valid_nums[0]
  print get_wait_time(593)  # San Mateo