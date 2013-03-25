#!/usr/bin/env python

# file: notify.py
# author: tippenein

import os
import smtplib
import getpass
import json

config_path = os.path.join(os.getcwd(), '.smsnrc')
smtp_host   = 'smtp.gmail.com'
smtp_port   = 587


class SMS_Notify:

    def __init__(self):
        self.password = self.info_prompt()

    def info_prompt(self):
        if os.path.exists(config_path):
            d = self.get_config()
            email = d['email']
            password = getpass.getpass("What's the password for the account \
                                    {}\n>".format(email))
        else:
            d = {}
            d['email'] = raw_input("What's the email you'll be using? \n>")
            password = getpass.getpass("What's the password for that account \n>")
            choice = raw_input('''
            Which carrier are you sending to?
            1. Verizon
            2. T-Mobile
            3. Virgin Mobile
            4. Cingular
            5. Sprint
            7. Nextel
            >>
            ''')
            d['carrier'] = self.map_carrier(choice)
            d['phone'] = raw_input("What's the 10 digit phone number you're sending to?\n>")
            info = json.dumps(d)
            with open(config_path, 'w') as fd:
                fd.write(info)

        return password

    def get_config(self):
        with open(config_path, 'r') as fd:
            s = fd.read()
        return json.loads(s)

    def map_carrier(self, choice):
        exts = ['vtext.com', 'tmomail.net', 'vmobl.com', 'cingularme.com',\
                'messaging.sprintpcs.com','messaging.nextel.com']
        mapped = zip(range(1,8), exts)
        return [n[1] for n in mapped if n[0] == int(choice)]

    def send(self, text):
        '''
        '''
        d = self.get_config()
        send_from = d['email']
        send_to = "{}@{}".format(d['phone'], ''.join(d['carrier']))
        smtp = smtplib.SMTP( smtp_host, 587 )
        try: 
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(send_from, self.password )
            print "sending txt to {}".format(send_to)
            smtp.sendmail(send_from, send_to, text)
        except smtplib.SMTPException:
            #TODO refine this exception
            print "Sending to {} failed".format(send_to)

        smtp.close()


if __name__ == '__main__':
    notify = SMS_Notify()
    notify.send("oh hai")
