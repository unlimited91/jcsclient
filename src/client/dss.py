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
import xml.sax


##===================================
## Global vars
##===================================


# Set this value to 1 for debugging
DSS_DEBUG = 0

# valid list of actions 


dss_info  = {
    'op' : None,
    'action' : None,
    'bucket' : None,
    'prefix' : None,
    'object' : None,
    'sign'   : None,
    'printer': None,
    'src'   : None,
    'target'   : None,
    'dss_valid_action_list': ['ls', 'cp', 'rm', 'mb', 'rb', 'hb', 'ho'],
}
os.environ['REQUESTS_CA_BUNDLE'] = os.path.join('/etc/ssl/certs/','ca-certificates.crt')

##===================================
## Main workflow
##===================================

def initiate(argv):
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

    parse_dss_info(argv)
    ret = validate_args()
    if(ret < 0):
        sys.exit(ret)
    dss_info['sign'] = gets_dss_signature()
    make_dss_request()
    return



##===================================
## Parses received arguments
##===================================

def parse_dss_info(argv):
    global dss_info
    if(len(argv) < 3):
        valid_dss_actions()
        return 0
    # starting index of dss params
    dss_params_start_index = 2
    # printer , default is prettyprint
    printer = "prettyprint"
    if(argv[2].lower() == "dss"):
        dss_params_start_index = 3
        printer = argv[1][2:]
    
    # check for number of paramateres
    if((argv[2].lower() == "dss" and len(argv) < 4) or (argv[1].lower() == "dss" and len(argv) < 3)):
        print "ERROR: Not enough parameters specified for DSS service!"
        valid_dss_actions()
        sys.exit(1)

    action  = argv[dss_params_start_index]
    if(action == "help" or action not in dss_info['dss_valid_action_list']):
        valid_dss_actions()
        sys.exit(1)
    src = None
    target = None
    if(len(argv) == dss_params_start_index + 3):
        src = argv[dss_params_start_index + 1]
        target = argv[dss_params_start_index + 2]
    elif(len(argv) == dss_params_start_index + 2):
        target = argv[dss_params_start_index + 1]
    elif(len(argv) == dss_params_start_index + 1):
        target = 'dss:///'
    else:
        print "ERROR: Wrong number of parameters specified for DSS service!"
        valid_dss_actions()
        sys.exit(1)

    whisper("DSS code received:\nPrinter: " + str(printer) + "\nAction: " + str(action) + "\nTarget: " + str(target) + "\n")


    dss_info['action'] = action
    dss_info['printer'] = printer
    dss_info['src'] = src
    dss_info['target'] = target
    dss_info['op'] = dss_op_from_action(action)
    target = ''
    if(dss_info['action'] == 'cp' and dss_info['op'] == 'GET'):
        target = dss_info['src'].replace("dss://","")
    else:
        target = dss_info['target'].replace("dss://","")
    pos = target.find('/')
    # If there is no '/' in target, its just a bucket name, cant populate obj
    # If it ends with /, its again just bucket name
    if(dss_info['action'] != 'ls'):
        if pos != -1 and not target.endswith('/'):
            dss_info['bucket'] = target[0:pos]
            dss_info['object'] = target[pos + 1:]
        else:
            if target.endswith('/'):
                dss_info['bucket'] = target[0:pos]
            else:
                dss_info['bucket'] = target
    else:
        if pos != -1: 
            dss_info['bucket'] = target[0:pos]
            if(pos < len(target) -1):
                dss_info['prefix'] = target[pos+1:]
        else:
            if target.endswith('/'):
                dss_info['bucket'] = target[0:pos]
            else:
                dss_info['bucket'] = target




def is_valid_dss_path(path):
    # TODO: more checks to come
    return path.startswith("dss://")

def is_valid_dss_bucket_path(path):
    if(is_valid_dss_path(path)):
        bucket_path = path.replace("dss://", "")
        pos = bucket_path.find('/')
        # case  1 : / in between
        if(pos != -1 and not bucket_path.endswith('/')):
            return False
        # case 2: / at end
        if(pos != -1 and pos == len(bucket_path) -1):
            return True
        # case 3 : no /
        if(pos == -1):
            return True
        return False
    else:
        return False

def is_valid_dss_object_path(path):
    # there should be atlease one / and it should not be at the end
    if(is_valid_dss_path(path)):
        object_path = path.replace("dss://", "")
        pos = object_path.find('/')
        if(pos != -1 and not object_path.endswith('/')):
            return True
        else:
            return False
    else:
        return False



def is_valid_local_path(path):
    # TODO: more checks to come
    return not (path.startswith("dss://"))

def validate_args():
    global dss_info

    # check for valid printer 
    if(dss_info['printer'] not in ['curl', 'prettyprint']):
        print "Only --curl and --prettyprint allowed as first argument!"
        return -1

    # check for valid actions
    if(dss_info['action'] not in dss_info['dss_valid_action_list']):
        print dss_info['action'] + " is not a valid command"
        return -1

    # check for args based on the actions
    action = dss_info['action']
    src = dss_info['src']
    target = dss_info['target']
    if(action == 'ls' or action == 'rm' or action == 'rb' or action == 'mb' or action == 'hb' or action == 'ho'):
        if( not is_valid_dss_path(target)):
            print target + " is a not a valid dss path"
            return -1
    elif(action == 'cp'):
        if(is_valid_dss_path(src) and is_valid_dss_path(target)):
            print "both source and target cannot be dss paths"
            return -1
        elif(is_valid_local_path(src) and is_valid_local_path(target)):
            print "both source and target cannot be local paths"
            return -1
    
    if(action == 'rm' or action == 'ho'):
        # target path should be object
        if(not is_valid_dss_object_path(target)):
            print "for action " + action + " target path " + target + " should be a object"
            return -1

    if(action == 'mb' or action == 'rb' or action == 'hb'):
        # target path should be bucket
        if(not is_valid_dss_bucket_path(target)):
            print "for action " + action + " target path " + target + " should be a bucket"
            return -1

    if(action == 'cp'):
        # dss target path should be object
        if(is_valid_dss_path(src) and not is_valid_dss_object_path(src)):
            print "for action " + action + " source path " + src + " should be a object"
            return -1
        if(is_valid_dss_path(target) and not is_valid_dss_object_path(target)):
            print "for action " + action + " target path " + target + " should be a object"
            return -1
    return 0


##===================================
## Prints debug logs when DSS_DEBUG is set
##===================================

def whisper(mystr):
    if DSS_DEBUG == 1:
        print "DEBUG: " + mystr
    return

##===================================
## Returns HTTP verb from DSS action
##===================================

def dss_op_from_action(action):
    global dss_info
    if action in ['mb']:
        return 'PUT'
    if action in ['ls']:
        return 'GET'
    if action in ['hb', 'ho']:
        return 'HEAD'
    if action in ['rm', 'rb']:
        return 'DELETE'
    if action in ['cp']:
        if(is_valid_dss_path(dss_info['src']) and is_valid_local_path(dss_info['target'])):
            return 'GET'
        if(is_valid_dss_path(dss_info['target']) and is_valid_local_path(dss_info['src'])):
            return 'PUT'
    return None

##===================================
## Prints a list of DSS actions
##===================================

def valid_dss_actions():
    print "Valid actions for DSS:"
    print "\tls:    Lists all the buckets created for a user or all the objects in the bucket e.g. jcs dss ls, jcs dss ls dss://<bucket-name>"
    print "\tmb:    Creates the bucket mentioned in the target path e.g. jcs dss mb dss://<bucket-name>"
    print "\trb:    Deletes the bucket mentioned in the target path e.g. jcs dss rb dss://<bucket-name>"
    print "\thb:    Lists details of the bucket mentioned in the target path e.g jcs dss hb dss://<bucket-name>"
    print "\tcp:    Uploads or downloads object e.g. jcs dss cp <src-path> <target-path>"
    print "\t       if <src-path> is dss path and <target-path> is local path, download is done e.g jcs cli cp dss://bucket1/object1 /home/user1/object1"
    print "\t       if <src-path> is local path and <target-path> is dss path, upload is done e.g jcs cli cp /home/user1/object1 dss://bucket1/object1"
    print "\tho:    Lists details of the object mentioned in target path e.g. jcs dss rb dss://<bucket-name>"
    print "\trm:    Deletes the object mentioned in target path e.g. jcs dss rm dss://<bucket-name>/<object-name>"
    return

##===================================
## Returns cannonical string
##===================================

def gets_dss_cannonical_str():
    cannonical_str = ''
    md5_checksum   = ''
    date           = formatdate(usegmt=True)
    content_type   = 'application/octet-stream'
    path           = gets_dss_path_for_cannonical_str()

    cannonical_str += dss_info['op']
    cannonical_str += "\n" + md5_checksum
    if dss_info['action'] == 'cp' and dss_info['op'] == 'PUT':
        cannonical_str += "\n" + content_type
    else:
        cannonical_str += "\n"
    cannonical_str += "\n" + date
    cannonical_str += "\n" + path
    return cannonical_str

##===================================
## Signs and build Auth header
##===================================

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

##===================================
## Builds the path DSS recognizes
##===================================

def gets_dss_path_for_cannonical_str():
    path = ''
    if (dss_info['bucket'] is None or len(dss_info['bucket']) == 0):
        path = '/'
    else:
        path += '/' + dss_info['bucket']
    if dss_info['object'] is not None:
        path += '/' + dss_info['object']
    return path


def gets_dss_path():
    path = ''
    if (dss_info['bucket'] is None or len(dss_info['bucket']) == 0):
        path = '/'
    else:
        path += '/' + dss_info['bucket']
        #if(dss_info['action'] == 'ls'):
        #    path += "?max-keys=1000000000"
    if dss_info['object'] is not None:
        path += '/' + dss_info['object']
    if dss_info['prefix'] is not None:
        path += '?prefix=' + dss_info['prefix']
    return path



class ListBucketHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.name = ""
        self.size = ""
        self.modified = ""
    
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if tag == "Size":
            modified_len = len(self.modified)
            space1 = "\t"
            if(modified_len  < 32):
                space1 = " " * (32 - modified_len)
            size_len = len(self.size)
            space2 = "\t"
            if(size_len  < 16):
                space2 = " " * (16 - size_len)
            print self.modified + space1 + self.size + space2 + self.name

    def characters(self, content):
        if self.CurrentData == "Key":
            self.name = content
        elif self.CurrentData == "Size":
            self.size = content
        elif self.CurrentData == "LastModified":
            self.modified = content


class ListAllMyBucketsHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.name = ""
        self.created = ""
    
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if tag == "CreationDate":
            created_len = len(self.created)
            space = "\t"
            if(created_len  < 32):
                space = " " * (32 - created_len)
            print self.created + space + self.name

    def characters(self, content):
        if self.CurrentData == "Name":
            self.name = content
        elif self.CurrentData == "CreationDate":
            self.created = content

class ErrorHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.error_code = ""
    
    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        if tag == "Code":
            print "Error code : " + self.error_code

    def characters(self, content):
        if self.CurrentData == "Code":
            self.error_code = content




##==========================================
## Makes request to DSS and parses response
##==========================================

def make_dss_request():
   
    whisper("DSS INFO : " + str(dss_info))

    ## Build headers
    headers = {
        'Authorization': None,
        'Date': None,
    }
    headers['Authorization'] = dss_info['sign']
    headers['Date'] = formatdate(usegmt=True)
    # Action specific headers
    if dss_info['action'] == 'cp' and dss_info['op'] == 'PUT':
        try:
            
            statinfo = os.stat(dss_info['src'])
            headers['Content-Length'] = statinfo.st_size
            headers['Content-Type'] = 'application/octet-stream'
        except:
            print "Error in getting file stats: " + str(sys.exc_info())
            sys.exit(0)

    ## Build URL and send request
    url = common.global_vars['dss_url']
    url += gets_dss_path()
    resp = ''
    whisper("URL : " + url)
    whisper("Headers : " + str(headers))
    if (dss_info['printer'] == 'curl'):
        # If user picked curl, make his a nice curl string and exit
        curl_str = "curl -i -v -X " + dss_info['op'] + " -H \'Authorization: " + \
                   dss_info['sign'] + "\' " + "-H \'Date: " + headers['Date'] + "\' " + url
        print curl_str
        return
    if dss_info['op'] == 'GET':
        if dss_info['action'] == 'cp':
            filname = dss_info['target']
            resp = download_file(filname, url, headers)
        else:
            resp = requests.get(url, headers=headers, verify=common.global_vars['is_secure'])
    elif dss_info['op'] == 'HEAD':
        resp = requests.head(url, headers=headers, verify=common.global_vars['is_secure'])
    elif dss_info['op'] == 'DELETE':
        resp = requests.delete(url, headers=headers, verify=common.global_vars['is_secure'])
    elif dss_info['op'] == 'PUT':
        if dss_info['action'] == 'cp':
            data = open(dss_info['src'], 'rb')
            resp = requests.put(url, headers=headers, data=data, verify=common.global_vars['is_secure'])
        if dss_info['action'] == 'mb':
            resp = requests.put(url, headers=headers, verify=common.global_vars['is_secure'])
    else:
        print "Unexpected operation!"
        sys.exit(0)


    ## Parse output
    if resp.status_code >= 400:
        print "Request failed"
        print 'HTTP error code: %s' % resp.status_code
        try:
            rawxmlret = resp.content
            parser = xml.sax.make_parser()
            parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            Handler = ErrorHandler()
            parser.setContentHandler(Handler)
            xml.sax.parseString(rawxmlret, Handler)
        except Exception:
            sys.exit(-1)
        

    else:
        rawheaders = {}
        rawheaders.update(resp.headers)
        #parsedheaders = json.loads(rawheaders)
        #print json.dumps(parsedheaders, indent=4, sort_keys=True
        if(dss_info['action'] in ['hb', 'ho']):
            for k,v in rawheaders.items():
                print k + ": " + v 

            #print rawheaders

    # GetObject iterates over the content and finishes it off
    if dss_info['action'] != 'cp':
        rawxmlret = resp.content
        #xmlret = xml.dom.minidom.parseString(rawxmlret)
        #print xmlret.toprettyxml()
        #return
        #print dss_info['bucket']
        if (dss_info['printer'] == 'prettyprint' and len(rawxmlret) != 0):
            if(dss_info['action'] == 'ls'):
                Handler = None
                parser = xml.sax.make_parser()
                parser.setFeature(xml.sax.handler.feature_namespaces, 0)
                if(len(dss_info['bucket']) == 0):
                    Handler = ListAllMyBucketsHandler()
                else:
                    Handler = ListBucketHandler()

                parser.setContentHandler(Handler)
                xml.sax.parseString(rawxmlret, Handler)
            elif(resp.status_code < 400):
                xmlret = xml.dom.minidom.parseString(rawxmlret)
                print xmlret.toprettyxml()
            #parser = xml.sax.make_parser()
            #parser.setFeature(xml.sax.handler.feature_namespaces, 0)
            #Handler = ListBucketHandler()   
            #parser.setContentHandler(Handler)
            #xml.sax.parseString(rawxmlret, Handler)


    if(resp.ok):
        print "Request successfully executed"
    return

##===================================
## Downloads object as file
##===================================

def download_file(filname, url, headers):
    with open(filname, 'wb') as handle:
        resp = requests.get(url, headers=headers, stream=True, verify=common.global_vars['is_secure'])
        if not resp.ok:
            print "Error downloading file " + dss_info['object']
            return resp
        for block in resp.iter_content(1024):
            handle.write(block)
    return resp
