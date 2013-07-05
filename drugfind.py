#!/usr/bin/python

from apiclient.discovery import build
from optparse import OptionParser
from apiclient import discovery
from apiclient import model
import json
import urllib


DEVELOPER_KEY = 'AIzaSyCPHiZ56l5VIGzWTRWAszNbJZzDFkRH0wU'
SERVICE_NAME = "youtube"
API_VERSION = "v3"
SEARCH_URL = "https://www.googleapis.com/freebase/v1/search?%s&filter=(any type:/medicine/drug)"

def get_id(options):
  fparams = dict(query=options.query, key=DEVELOPER_KEY)
  f_url = SEARCH_URL % urllib.urlencode(fparams)
  f_response = json.loads(urllib.urlopen(f_url).read())

  if len(f_response["result"]) == 0:
    exit("No matching terms were found in Freebase.")

  mids = []
  index = 1
  print "The following drugs were found:"
  for result in f_response["result"]:
    mids.append(result["mid"])
    print "  %2d. %s (%s)" % (index, result.get("name", "Unknown"),result.get("notable", {}).get("name", "Unknown"))
    index += 1

  mid = None
  while mid is None:
    index = raw_input("Enter a topic number to find related YouTube : ")
    try:
      mid = mids[int(index) - 1]
    except ValueError:
      pass
  return mid

def search(mid):
  service_url = 'https://www.googleapis.com/freebase/v1/topic'
  topic_id = mid
  params = {
    'key': DEVELOPER_KEY,
    'filter': '/medicine'
  }
  url = service_url + topic_id + '?' + urllib.urlencode(params)
  topic = json.loads(urllib.urlopen(url).read())
  keys = topic['property'].keys() 
  index =1
  for key in keys:
    print "  %2d. %s"%(index , key.split('/') [-1].replace('_',' '))
    index += 1

  propertunum = None
  while propertunum is None:
    index = raw_input("Enter a property number to find info or 0 to exit: ")
    if int(index) == 0:
      propertunum = 0
      break
    elif int(index) > len(keys) :
      print 'You have entered a invaild number'
    else:
      try:
        propertyname = keys[int(index) - 1]
        innerindex = 1
        for value in topic['property'][propertyname]['values']:
          print "  %2d. %s"%(innerindex , value['text'])
          innerindex += 1
      except ValueError:
        pass
  

if __name__ == "__main__":
  parser = OptionParser()
  parser.add_option("--query", dest="query", help="Freebase search term",
    default="Google")
  (options, args) = parser.parse_args()

  mid = get_id(options)
  search(mid)