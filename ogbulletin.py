from bs4 import BeautifulSoup
import urllib2
import smtplib
import sys
import unidecode

recipientList = ['corey.steele@highpointnetworks.com']

response = urllib2.urlopen('http://ogorman.sfcss.org/1001')
content = response.read()
soup = BeautifulSoup(content, 'html.parser')
bulletin = soup.find("article", {"id": "1001"}).get_text()

for recipient in recipientList:
    smtp = smtplib.SMTP("smtp.midco.net")
    message = """\
From: %s
To: %s
Subject: %s
    
%s""" % ( "thesteeles@midco.net", recipient, "OG Daily Bulletin", unidecode.unidecode(bulletin) )
    smtp.sendmail("thesteeles@midco.net", recipient, message)
    smtp.quit()

sys.exit(0)