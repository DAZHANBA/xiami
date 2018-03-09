# -*- coding: utf-8 -*-
"""
basic function for xiami
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time

# pre
# get script folder path
script_path = sys.path[0]
# print script_path
global v_step
v_step = 0
global tmp_log
tmp_log = ''

def file_write(content,file_name,mode='w'):
    with open(script_path+'\\'+file_name,mode) as f:
        f.write(content)
    print 'already written to %s' %file_name

def log_step(v_log):
    global v_step
    global tmp_log
    v_log = u"<%s> #%s: %s\n" %(time.ctime(), v_step, v_log)
    print 'v_log'
    tmp_log += v_log
    # print 'tmp_log: %s' %tmp_log
    file_write(v_log,'log.txt','a')
    v_step +=1
    return tmp_log

def project_log():
    """
    backup
    """
    file_write(tmp_log,'log.txt','a')
    print 'written to project_log'
