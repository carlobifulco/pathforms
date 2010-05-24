#!/usr/bin/env python
# encoding: utf-8
"""
web_email.py

Created by carlo Bifulco on 2009-01-23.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from google.appengine.ext import webapp
import cgi
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import mail
from web_publish import web_publish


class EmailSender(webapp.RequestHandler):
  """ email sending """



  def post(self):
    text=""
    recipient=""
    case_number=cgi.escape(self.request.get('case_number'))
    content="""<html>
      <head></head>
      <body>"""
    content+=cgi.escape(self.request.get('form_results'))
    content+="""</body></html> """

    
    text+= "me"
    user=str(users.get_current_user())
    text+= case_number
    text+= content
    q = db.GqlQuery("SELECT * FROM Settings WHERE user = :1", users.get_current_user())
    if q.get():
      user_setting=q.get()
      recipient=user_setting.recipient_email
    else:
      self.redirect("/setup")
    message = mail.EmailMessage(sender=users.get_current_user().email(),
                                subject=case_number)
    text+= recipient

    message.to = recipient
    message.html = content
    
    text+="ERROR="
    text+= str(message.check_initialized())
    text+=str(message.__dict__)
    text+=dir(message)
    message.send()
    self.response.out.write(web_publish(text))


def main():
	pass


if __name__ == '__main__':
	main()

