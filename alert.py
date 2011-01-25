# -*- coding: UTF8 -*-
'''
Created on 20/01/2011

@author: rosaldanha
'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import os
import config

class Alert(object):
    '''
    classdocs
    '''
    gmail_user = "bkp.ptms@gmail.com"
    gmail_pwd = "bkp.ptms@."
    smtp_user = "prt4.ptm006"
    smtp_pwd = "prt4.ptm006@."

    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def mail(self, subject, text, attach):
        msg = MIMEMultipart()
        msg.set_charset('utf-8')
        to = ''
        msg['From'] = self.gmail_user
        for e in config.EMAIL_RCPT_LIST:
            to += e + ','
        msg['To'] = to 
        msg['Subject'] = subject
        
        msg.attach(MIMEText(text.encode('utf-8', 'ignore')))
        
        if attach != None:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(attach, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                    'attachment; filename="%s"' % os.path.basename(attach))
            msg.attach(part)
        
        mailServer = smtplib.SMTP("mail.mpt.gov.br",25)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(self.smtp_user, self.smtp_pwd)
        
        mailServer.sendmail(self.smtp_user, config.EMAIL_RCPT_LIST , msg.as_string())
        # Should be mailServer.quit(), but that crashes...
        mailServer.close()
# -------------------------------------------------






#mail("some.person@some.address.com",
#   "Hello from python!",
#   "This is a email sent with python",
#   "my_picture.jpg")