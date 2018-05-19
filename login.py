# -*- coding: utf-8 -*-
"""
for xiami daily login
version 0.3
upgrade chromedriver
TODO: use decorator
TODO: mail notification - done
TODO: mail specific log - done
TODO: all path join in different platform - done
TODO: config in XML - done
TODO: if '24bc' in tmp
"""

import sys
reload(sys)
sys.setdefaultencoding('utf8')
import re
from selenium import webdriver
from basic import *
import mail
import time

"""
# pre
# get script folder path
SCRIPT_PATH = sys.path[0]
# print SCRIPT_PATH
v_step = 0

def file_write(content,file_name,mode='w'):
    with open(SCRIPT_PATH+'\\'+file_name,mode) as f:
        f.write(content)
    print 'already written to %s' %file_name

def log_step(v_log):
    global v_step
    v_log = u"<%s> #%s: %s\n" %(time.ctime(), v_step, v_log)
    print v_log
    file_write(v_log,'log.txt','a')
    v_step +=1
    """

# mail config
receivers = [str(TO_USER)]
print 'receivers: %s' %receivers

subject = time.strftime("%Y-%m-%d",time.localtime())+' xiami login status'

log_step('xiami_login - Begin -') #step 0

email = str(XIAMI_USER)
print 'XIAMI_USER: %s' %XIAMI_USER
password = str(XIAMI_PW)
print 'XIAMI_PW: %s' %XIAMI_PW
code = str(CODE)
print 'CODE: %s' %CODE

# diferent by machine
chrome_driver_path = str(PATH_SELENIUM)

login_pat = re.compile(ur'//www.xiami.com/web\?(\d*)">首页</a>',re.I) # http://www.xiami.com/web?
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
    if CODE in tmp:
        file_write(tmp,'source_home.html')
        log_step('already logined xiami_home') #step 4
        break

try:    
    main_seq = login_pat.search(tmp).group(1)
    main_url = u'http://www.xiami.com/web?' + main_seq
    print "main_url: %s" %main_url
    log_step('get main_url: %s' %main_url) #step 5
except:
    log_step('error!main_url parsing failed') #step 5
    driver.quit()
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
            driver.quit()
            log_step('already checkin for %s days' %checkin_day) 
            detail = log_step('xiami_login - Over -') #step final, fetch tmp_log
            
            # start send mail
            content = 'already checkin for %s days\ndetail:\n%s' %(checkin_day,detail)
            # print content
            tmp_mail = mail_draft.MailSend(MAIL_SMTP,MAIL_PORT,MAIL_USER,MAIL_PW)
            tmp_mail.send(receivers,subject,content)
            
            """
            mail.MailSend().send(['987663805@qq.com'],'xiami login status',\
            ('already checkin for %s days\ndetail:\n%s' %(checkin_day,tmp_log)))
            """
            break
    # project_log() # no need to have two logs
else:
    detail = log_step('error!get main page failed') #step 6, fetch tmp_log
    driver.quit()
    content = 'error! get main page failed\ndetail:\n%s' %detail
    tmp_mail = mail_draft.MailSend(MAIL_SMTP,MAIL_PORT,MAIL_USER,MAIL_PW)
    tmp_mail.send(receivers,subject,content)
    sys.exit()
    