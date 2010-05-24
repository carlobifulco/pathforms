#!/usr/bin/env python
# encoding: utf-8
"""
web_setup.py

Created by carlo Bifulco on 2009-01-23.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from google.appengine.ext import db
from google.appengine.ext import webapp
from web_data import localize
from google.appengine.api import users
from google.appengine.ext.webapp import template
from web_publish import web_publish
import cgi
from  web_data  import Settings



class SetupPage(webapp.RequestHandler):
  """ Main Intial Page of Application """


  def get(self):
    template_path = localize("setup.html")
    user = users.get_current_user()
    q = db.GqlQuery("SELECT * FROM Settings WHERE user = :1", user)
    #print q
    #userprefs = q.get()
   #  q=Settings.all().filter("user=",user)
    #print q, list(q),q.get(),list(Settings.all()), user,Settings.all()[1].__dict__
    if q.get():
      user_setting=q.get()
      text=template.render(template_path, {"entered":"",
                                            "email":user_setting.recipient_email,
                                            "header":user_setting.header,
                                            "line_start":user_setting.line_start})
    else:
      text=template.render(template_path, {"entered":"","email":"", "header":"","line_start":""})
    self.response.out.write(web_publish(text))
    
class EnterSetup(webapp.RequestHandler):



  def get(self):
    user = users.get_current_user()
    recipient_email=cgi.escape(self.request.get('recipient_email'))
    header=cgi.escape(self.request.get('header'))
    line_start=cgi.escape(self.request.get('line_start'))
    q = db.GqlQuery("SELECT * FROM Settings WHERE user = :1", user)
    if q.get():
      user_setting=q.get()
    else:
      user_setting=Settings()
    user_setting.recipient_email=recipient_email
    user_setting.line_start=line_start
    user_setting.header=header
    user_setting.put()
    template_path = localize("setup.html")
    text=template.render(template_path, {"entered":"OK",
                                          "email":user_setting.recipient_email,
                                          "header":user_setting.header,
                                          "line_start":user_setting.line_start})
    self.response.out.write(web_publish(text))
    q = db.GqlQuery("SELECT * FROM Settings WHERE user = :1", user)
    #print list(q), q.get()#
    #print q.get().__dict__

def main():
	pass


if __name__ == '__main__':
	main()

