#!/usr/bin/env python

import os
import subprocess
from lxml import etree

DMV_OFFICES_URL = ""

def download(refresh = False):
  outfile = "offices.xml"
  try:
    os.stat(outfile)
    print 'Using cached copy of', outfile
  except Exception, e:
    refresh = True
  if refresh:
    subprocess.check_call(['curl','-o',outfile,'http://apps.dmv.ca.gov/fo/offices/appl/fo_data/foims_XmlFOdata.xml'])
def downloadWait(index,refresh = False):
  outfile = "xmlhttprequest_%04d.xml" % index
  try:
    os.stat(outfile)
    print 'Using cached copy of', outfile
  except Exception, e:
    refresh = True
  if refresh:
    subprocess.check_call(['curl','-o',outfile,'http://apps.dmv.ca.gov/fo/offices/apps/foGeoXml_v2.jsp?foNumb='+str(index)])

def getNums():
  foims = open('offices.xml','rb')
  tree = etree.parse(foims)
  foims.close()
  root = tree.getroot()
  results = []
  children = root.iter()
  first = children.next()
  if first.tag != 'offices':
    print "Ugh, the structure has changed!"
    return []
  for child in children:
    if child.tag != 'fo_office':
      print 'Bad child.', child
      continue
    results.append(int(child.attrib['num'],10))
  return results
def getWait(index):
  infile = "xmlhttprequest_%04d.xml" % index
  xmlhr = open(infile,'rb')
  tree = etree.parse(xmlhr)
  xmlhr.close()
  root = tree.getroot()
  hour, mins = root.find('./fo_office/nonAppt').text.split(':')
  return int(hour,10) * 60 + int(mins,10)

download()
validNums = getNums()
if len(validNums) != len(set(validNums)):
  print "Some office indices repeat!"
#print validNums
#print len(validNums)
print validNums[0]
downloadWait(593)
print getWait(593)
