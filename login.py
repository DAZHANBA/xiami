# -*- coding: utf-8 -*-
"""
for xiami daily login
version 0.2
TODO: use decorator
TODO: mail notification
"""
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
from selenium import webdriver
import time
import os

# pre
# get script folder path
script_path = sys.path[0]
# print script_path
v_step = 0

def file_write(content,file_name,mode='w'):
    with open(script_path+'\\'+file_name,mode) as f:
        f.write(content)
    print 'already written to %s' %file_name

def log_step(tmp_log):
    global v_step
    tmp_log = u"<%s> #%s: %s\n" %(time.ctime(), v_step, tmp_log)
    print tmp_log
    file_write(tmp_log,'log.txt','a')
    v_step +=1

log_step('- Begin -') #step 0

email = ''
password = ''
# diferent by machine
chrome_driver_path = r''

login_pat = re.compile(ur'<a href="http://www.xiami.com/web\?(\d*)">首页</a>',re.I)
checkin_pat = re.compile(ur'已连续签到(.*)天',re.I)

xiami_web_url = r'http://m.xiami.com/web'

log_step('ini config ready') #step 1

driver = webdriver.Chrome(chrome_driver_path)

log_step('driver ready') #step 2

driver.get(xiami_web_url)

log_step('already logined xiami_web') #step 3

file_write(driver.page_source,'source_login.html')

driver.find_element_by_name('email').send_keys(email)
driver.find_element_by_name('password').send_keys(password)

while True:
    driver.find_element_by_name('LoginButton').click()
    time.sleep(0.5)
    tmp = driver.page_source
    if u'24BC' in tmp:
        file_write(tmp,'source_home.html')
        log_step('already logined xiami_home') #step 4
        break

try:    
    main_seq = login_pat.search(tmp).group(1)
    main_url = u'http://www.xiami.com/web?' + main_seq
    log_step('get main_url: %s' %main_url) #step 5
except:
    log_step('error!main_url parsing failed') #step 5
    sys.exit()


driver.get(main_url)
tmp = driver.page_source
file_write(tmp,'source_main.html')


if u'好友近况' in tmp:
    log_step('already logined xiami_main') #step 6
    while True:
        try:
            checkin_day = checkin_pat.search(tmp).group(1)
        except:
            while True:
                try:
                    driver.find_element_by_class_name('check_in').click()
                    time.sleep(0.5)
                except:
                    log_step('checkin click over') #step 7
                    break
            tmp = driver.page_source
            file_write(tmp,'source_main_checkin.html') 
        else:
            log_step('already checkin for %s days' %checkin_day)
            log_step('- Over -') #step final
            driver.quit()
            break
else:
    log_step('error!get main page failed') #step 6
    driver.quit()
    sys.exit()
    #TODO: mail notification