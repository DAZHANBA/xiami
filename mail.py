# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from basic_draft import *

class MailSend(object):
    """
    host = 'smtp.sina.com'
    port = 587
    user = 'dazhanba16@sina.com'
    password = '1990927'
    """
    def __init__(self, host, port, user, password):
        self.host = str(host)
        self.port = int(port)
        self.user = str(user)
        self.password = str(password)
        
    def connect(self):
        try:
            s = smtplib.SMTP(self.host,self.port)
            s.login(self.user,self.password)
        except:
            log_step('login smtp server failed')
            return 0
        else:
            log_step('already login smtp server')
            return s
    
    def send(self,receivers,subject,body):
        s = self.connect()
        if s:
            msg = MIMEText(body,'text','utf-8') #中文需参数‘utf-8’，单字节字符不需要    
            msg['From'] = self.user
            msg['To'] = ','.join(receivers)
            msg['Subject'] = Header(subject, 'utf-8')
            try:
                log_step('MailSend - Begin -')
                s.sendmail(self.user,receivers,msg.as_string())
            except:
                log_step('send mail failed')
                log_step('MailSend - Over -')
                return 0
            else:
                log_step("""From:%s; To:%s; Subject:%s; Body:%s; send mail successfully""" 
                %(self.user,','.join(receivers),subject,body))
                log_step('MailSent - Over -')
                return 1
        else:
            log_step('MailSend - Over -')
            return 0


if __name__ == '__main__':
    x = MailSend('smtp.sina.com',587,'dazhanba16@sina.com','1990927')
    x.send(['987663805@qq.com'],'test','test')





"""
receivers = ['987663805@qq.com']
# 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
message = MIMEText('Python 邮件发送测试...', 'plain', 'utf-8')
subject = 'Python SMTP 邮件测试'
connect = smtplib.SMTP(smtp_host,port)
connect.login(user, password)
connect.quit()
"""
