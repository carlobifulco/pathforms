#!/usr/bin/env python
# encoding: utf-8
"""
web_data.py

Created by carlo Bifulco on 2009-01-23.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from google.appengine.ext import db
import cgi

def localize(file_name):
  return os.path.join(os.path.dirname(__file__),file_name)

def make_ints(strings_list):
  return [int(i) for i in strings_list] 
  
  
def test_yaml_validity(text):
  try:
    t=yaml.load(text)
  except:
    return False
  return True


class Form (db.Model):
  author = db.UserProperty()
  title=db.StringProperty()
  content = db.TextProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  
  
def localize_dir(fine_name):
    print __file__,"HERE 1", os.path.abspath(__file__)
    py_dir=os.path.dirname(os.path.abspath(__file__))
    print py_dir
    os.chdir(py_dir)


class Settings(db.Model):
  user = db.UserProperty()
  recipient_email=db.StringProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  header=db.StringProperty()
  line_start=db.StringProperty()
  
  
  
def get_form_content(title):
  return Form.all().filter("title =",title).order("-date").get().content

def get_form(title):
  return Form.all().filter("title =",title).order("-date").get()

  


def main():
	pass


if __name__ == '__main__':
	main()

