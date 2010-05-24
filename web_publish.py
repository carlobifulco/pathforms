#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2006-2008 Carlo Bifulco
# See LICENSE for details.




def header():
    return """
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd"><strong strong=true></strong>
<html>
  <head>

  
  <script type="application/x-javascript"  src="css/jquery-latest.js"/></script>


  

  
  
  
  <style type="text/css" media="screen">


    
  textarea {
  font: 100% Monaco, "Courier New", Courier, monospace;
  border: 1px solid #ddd;
  border-color:#666 #ddd #ddd #666;
  color: Black;
  width: 100%;
  }
    
   

  #footer {
  font-size:85%;
    position: float;
    width: auto;
    height: auto;
    top: auto;
    right: 0;
    bottom: 0;
    left: 0;
  }
  


  
  </style>
  </head>
  <body>
  <div id="header" class="ui-layout-north ui-layout-pane ui-layout-pane-north open" pane="north">
  <table
 style="text-align: left; background-color: wheat; width: 640px; height: 20px;"
 border="0" cellpadding="0" cellspacing="0">
    <tbody>
      <tr>
        <td><small><a href="/">Home</a></small></td>
        <td style="background-color: rgb(255, 204, 153);"></td>
        <td><small><a href="/setup">Setup</a></small></td>
        <td><a href="/help"><small>Help</a></small></td>
        <td></td>
      </tr>
    </tbody>
  </table>
  </div>
  <br>

  """

def footing():
    return """
        <div id="footer"
    
        <table style="text-align: left; background-color: wheat; width: 640px; height: 20px;"
        border="0" cellpadding="0" cellspacing="0">
          <td><small><h8><p>(c) Copyright 2009 Carlo  Bifulco. All Rights Reserved.</p> </h8></small></td>
          <td style="background-color: rgb(255, 204, 153);"></td>
          <td>       <img src="http://code.google.com/appengine/images/appengine-silver-120x30.gif"
                  alt="Powered by Google App Engine" /></td>
          <td></td>
          <td></td>
          </tr>
          </table>
   
        </div>
  </body>
</html>
"""

def web_publish(text):
    return header()+text+footing()




def main():
    pass


if __name__ == '__main__':
    main()

