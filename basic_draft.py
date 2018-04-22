# -*- coding: utf-8 -*-
"""
basic function for xiami
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
from lxml import etree
# import xml.dom.minidom
# import re
import os

# pre
# get script folder path
SCRIPT_PATH = sys.path[0]
# print SCRIPT_PATH

# read config
with open ("config.xml") as f:
    config = f.read()

config_xml = etree.XML(config)
PATH_LOG = config_xml.xpath("//log[1]/text()")[0]


global v_step
v_step = 0
global tmp_log
tmp_log = ''

"""
def trim(string):
    return re.sub(r' |\n','',string)

DOMTree = xml.dom.minidom.parse("config.xml")
collection = DOMTree.documentElement
LOG = trim((collection.getElementsByTagName("log")[0]).childNodes[0].data)
"""

def file_write(content,file_name,mode='w'):
    # TODO: different path join in os and win - done
    with open(os.path.join(SCRIPT_PATH,file_name), mode) as f: 
        f.write(content)
    print 'already written to %s' %file_name

def log_step(v_log):
    global v_step
    global tmp_log
    global PATH_LOG
    v_log = u"<%s> #%s: %s\n" %(time.ctime(), v_step, v_log)
    print 'v_log: %s' %tmp_log
    tmp_log += v_log
    # print 'tmp_log: %s' %tmp_log
    file_write(v_log,PATH_LOG,'a')
    v_step +=1
    return tmp_log

def project_log():
    """
    backup
    """
    file_write(tmp_log,'log.txt','a')
    print 'written to project_log'
