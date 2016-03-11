import os
import sys
import time
import hmac
import json
import base64
import requests
import exceptions
import xml.dom.minidom
from hashlib import sha1
from client import common
from email.utils import formatdate

# Set this value to 1 for debugging
DSS_DEBUG = 0

dss_info  = {
    'op' : None,
    'action' : None,
    'bucket' : None,
    'object' : None,
    'sign'   : None,
    'printer': None,
}
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join('/etc/ssl/certs/','ca-certificates.crt')

def initiate(printer, action, target):
    global dss_info

    # Fetch access key, secret key and endpoints from env
    try:
        common.setup_client_from_env_vars()
        common._ensure_global_vars_populated()
        if common.global_vars['dss_url'] is None:
            print "Global variable dss_url not set!"
            raise Exception
    except Exception:
        print "You need to set environment variables: DSS_URL, ACCESS_KEY and SECRET_KEY to make a DSS request"
        sys.exit()

    parse_dss_info(printer, action, target)
    dss_info['sign'] = gets_dss_signature()
    make_dss_request()
    return

def parse_dss_info(printer, action, target):
    # Can populate a bucket name of zero length. Careful!
    global dss_info
    printer = printer[2:]
    action  = action[7:]
    if target is not None:
        target  = target[7:]
    else:
        target = '/'

    whisper("DSS code received:\nPrinter: " + str(printer) + "\nAction: " + str(action) + "\nTarget: " + str(target) + "\n")

    if printer not in ['curl', 'prettyprint']:
        print "Only --curl and --prettyprint allowed as first argument!"
        sys.exit(0)

    dss_info['action'] = action
    dss_info['printer'] = printer

    if target[0] == '/':
        target = target[1:]
    pos = target.find('/')
    # If there is no '/' in target, its just a bucket name, cant populate obj
    # If it ends with /, its again just bucket name
    if pos != -1 and not target.endswith('/'):
        dss_info['bucket'] = target[0:pos]
        dss_info['object'] = target[pos + 1:]
    else:
        if target.endswith('/'):
            dss_info['bucket'] = target[0:pos]
        else:
            dss_info['bucket'] = target
    dss_info['op'] = dss_op_from_action(action)
    whisper("PARSED INFO:\nOP: "+ str(dss_info['op']) + "\nBucket: " + str(dss_info['bucket']) + "\nObject: " + str(dss_info['object']) + "\n")

    # Reject unwanted params
    if dss_info['bucket'] in ['*'] or dss_info['object'] in ['*']:
        print "Wildcards not allowed in target value."
        sys.exit(0)

    if dss_info['op'] is None:
        print "No valid action provided for DSS service!"
        valid_dss_actions()
        sys.exit(0)

    if dss_info['action'] == 'ListAllMyBuckets':
        if len(dss_info['bucket']) > 0:
            print "ListAllMyBuckets only accepts \'/\' as target"
            sys.exit(0)
    return

def whisper(mystr):
    if DSS_DEBUG == 1:
        print "DEBUG: " + mystr
    return

def dss_op_from_action(action):
    if action in ['CreateBucket']:
        return 'PUT'
    if action in ['ListAllMyBuckets', 'ListBucket', 'GetObject']:
        return 'GET'
    if action in ['HeadBucket', 'HeadObject']:
        return 'HEAD'
    if action in ['DeleteBucket', 'DeleteObject']:
        return 'DELETE'
    return None

def valid_dss_actions():
    print "Valid actions for DSS:"
    print "\tListAllMyBuckets: Lists all the buckets created for a user"
    print "\tListBucket:       Lists the contents of the bucket mentioned in Target parameter"
    print "\tCreateBucket:     Creates the bucket mentioned in Target parameter"
    print "\tDeleteBucket:     Deletes the bucket mentioned in Target parameter"
    print "\tHeadBucket:       Lists details of the bucket mentioned in Target parameter"
    print "\tGetObject:        Fetches the object mentioned in Target parameter"
    print "\tHeadObject:       Lists details of the object mentioned in Target parameter"
    print "\tDeleteObject:     Deletes the object mentioned in Target parameter"
    return

def gets_dss_cannonical_str():
    cannonical_str = ''
    md5_checksum   = '' #TODO: Shivanshu: make a function to calculate this for put object
    date           = formatdate(usegmt=True)
    content_type   = 'application/octet-stream'
    path           = gets_dss_path()

    cannonical_str += dss_info['op']
    cannonical_str += "\n" + md5_checksum
    cannonical_str += "\n" #+ content_type
    cannonical_str += "\n" + date
    cannonical_str += "\n" + path
    return cannonical_str

def gets_dss_signature():
    secret = common.global_vars['secret_key']
    secret_str = (str(secret)).encode('utf-8')
    cstr = (gets_dss_cannonical_str()).encode('utf-8')

    dss_hmac = hmac.new(secret_str, digestmod=sha1)
    dss_hmac.update(cstr)
    b64_hmac = ((base64.encodestring(dss_hmac.digest()))).decode('utf-8').strip()
    auth = ("%s %s:%s" % ("JCS", common.global_vars['access_key'], b64_hmac))
    whisper("Cannonical string:\n" + cstr)
    whisper("Generated new signature: " + auth)
    return auth

def gets_dss_path():
    path = ''
    if (dss_info['bucket'] is None or len(dss_info['bucket']) == 0):
        path = '/'
    else:
        path += '/' + dss_info['bucket']
    if dss_info['object'] is not None:
        path += '/' + dss_info['object']
    return path

def make_dss_request():
    ## Try using curl and pretty print
    headers = {
        'Authorization': None,
        'Date': None,
    }

    headers['Authorization'] = dss_info['sign']
    headers['Date'] = formatdate(usegmt=True)
    url = common.global_vars['dss_url']
    url += gets_dss_path()
    resp = ''

    if (dss_info['printer'] == 'curl'):
        print "curl -i -v -X " + dss_info['op'] + " -H \'Authorization: " + dss_info['sign'] + "\' " + "-H \'Date: " + headers['Date'] + "\' " + url
        return

    if dss_info['op'] == 'GET':
        resp = requests.get(url, headers=headers)
    elif dss_info['op'] == 'HEAD':
        resp = requests.head(url, headers=headers)
    elif dss_info['op'] == 'DELETE':
        resp = requests.delete(url, headers=headers)
    elif dss_info['op'] == 'PUT':
        if dss_info['object'] is not None:
            # Put object is blocked from dss_op_from_action() itself.
            # A smart alec can give create bucket action and pass bucket/object
            print "Bad bucket name in create bucket!. Slash not allowed in bucket name."
            sys.exit(0)
        resp = requests.put(url, headers=headers)
    else:
        print "Unexpected operation!"
        sys.exit(0)

    if resp.status_code >= 400:
        print 'Error %s thrown' % resp.status_code
    else:
        rawheaders = {}
        rawheaders.update(resp.headers)
        #parsedheaders = json.loads(rawheaders)
        #print json.dumps(parsedheaders, indent=4, sort_keys=True)
        print rawheaders

    rawxmlret = resp.content
    if (dss_info['printer'] == 'prettyprint' and len(rawxmlret) != 0):
        if dss_info['action'] == 'GetObject':
            print resp.content
        else:
            xmlret = xml.dom.minidom.parseString(rawxmlret)
            print xmlret.toprettyxml()
    return
