#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2006-2008 Carlo Bifulco
# See LICENSE for details.



import yaml
import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from web_publish import web_publish
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import memcache
from google.appengine.ext.webapp import template
from google.appengine.api import mail
from web_setup import SetupPage
from web_setup import EnterSetup
from web_email import EmailSender
from web_data import localize
from web_data import test_yaml_validity
from web_data  import Form
from  web_data  import Settings
from web_data  import get_form_content
from web_data  import get_form
from web_data  import make_ints
import os
import multiple_options
from mako.template import Template,exceptions



  

                                     
                           

class Select(webapp.RequestHandler):
  """ Main Intial Page of Application """


  def get(self):
    user = users.get_current_user()
    if user:
      #self.response.headers['Content-Type'] = 'text/plain'
      template_path = localize("main_page_template.html")
      titles=[i.title for i in Form.all()]
      titles.sort()
      forms_titles={"forms_titles":titles}
      text=template.render(template_path, forms_titles)
      self.response.out.write(web_publish(text))
      #self.response.out.write('Hello, ' + user.nickname())
    else:
      self.redirect(users.create_login_url(self.request.uri))
    


       
class FormEntry(object):
  def __init__(self):
    template_path=localize("form_edit_template.html")
    self.form=template.render(template_path,{})

       
class ChooseForm(FormEntry,webapp.RequestHandler):
  
  def __init__(self):
    FormEntry.__init__(self)

  def get (self):
    new_file_name=cgi.escape(self.request.get('new_file_name'))
    old_form_choice=cgi.escape(self.request.get('old_form_choice'))
    personal_form_name=cgi.escape(self.request.get('personal_form_name'))
    shared_form_name=cgi.escape(self.request.get('shared_form_name'))
    edit_form_choice=cgi.escape(self.request.get('edit_form_choice'))
    if new_file_name:
      form=self.form %("",new_file_name)
     #cherrypy.session['fileName'] =os.path.join(FORMS_DIR,(new_file_name+GLOBBY))
      text="<h1>%s</h1>" %new_file_name
      text+= form 
      self.response.out.write( web_publish(text))
    else:
      if old_form_choice:
        self.redirect("/renderform?form_title=%s" %old_form_choice)
      if edit_form_choice:
        self.redirect("/editform?new_form_name=%s" %edit_form_choice)
        
        # if test_yaml_validity(get_form_content(old_form_choice)):
        # 
        #   #self.response.out.write( web_publish(yaml.dump(yaml.load(get_form_content(old_form_choice)))))
        # #print old_form_choice
        #   
        # else:
        #   #self.response.out.write( "<h1> ERROR </h1>"+new_file_name)
        #   self.redirect("/editform?new_form_name=%s" %old_form_choice)

          
        

        
class EditForm(FormEntry,webapp.RequestHandler):
  def __init__(self):
    FormEntry.__init__(self)
  
  def get(self):
    form_title=cgi.escape(self.request.get('new_form_name'))
    #print form_title
    content=get_form_content(form_title)
    form_start=self.form %(content,form_title)
    self.response.out.write( web_publish(form_start))
    

  
    
    
    
class DeleteAll(webapp.RequestHandler):
  def get(self):
    for i in Form.all():
      print i.date, "deleted"
      i.delete()
    for i in Settings.all():
      print i.date, "deleted"
      i.delete()
      
    

class SaveForm(webapp.RequestHandler):
  def post(self):
    #print  "RRREEEEQQUESTT",self.request
    new_form_content=cgi.escape(self.request.get('form_content'))
    new_form_name=cgi.escape(self.request.get('new_form_name'))
    #print "NEW FORM NAME =", new_form_name
    #print "GETTING CALLED"

      #print """ <h1> Error </h1>"""+self.edit()
  ##print "TEST"
    #print "PASSED TEST"
    if get_form(new_form_name):
      new_form=get_form(new_form_name)
    else:
      new_form=Form()
    if users.get_current_user():
      new_form.author = users.get_current_user()
    new_form.content=new_form_content
    new_form.title=new_form_name
    new_form.put()
    all_forms=Form.all()
    #print all_forms, "datatbase"
    #print list(all_forms)
    for i in all_forms:
      pass
      #print i.author, i.content, i.date, i.title
    if YamlValidator().failure(new_form_name):
      self.response.out.write(YamlValidator().failure(new_form_name))
    else:
      self.redirect("/")





    
class WebPages:
    """ Rendering of the unfilled forms, and others, abstract class"""
    def __init__(self):
        self.MultipleSelect=multiple_options.MultipleSelect()
        self.Input=multiple_options.Input()
        self.forms_template="""
        <%!
        import multiple_options
        import os
        multiple_select=multiple_options.MultipleSelect()
        multiple_input=multiple_options.Input()
        %>
<div id="main">
        <FORM action="renderselection" method="post">
        <% tot_index=-1 %>
        % for option_couple in yaml_form:
        <% 
        heading=option_couple[0]
        check_box_lines=option_couple[1]
        %>
         <table
        style="text-align: left; background-color: rgb(230, 230, 230); width: 400px; height: 20px;"
        border="0" cellpadding="0" cellspacing="0">
        <tbody>
        <tr align="left" valign="top">
            <td>${heading}</td>
                  </tr>
                </tbody></table>
                <div align="left" VALIGN="top" style="margin-left : 4pc;">
                    % for check_box_line in check_box_lines:
                        <% tot_index+=1 %>
                        <% 
                        check_box_line=multiple_select.parse_and_render(check_box_line,tot_index)
                        check_box_line=multiple_input.parse_and_render(check_box_line,tot_index)
                        %>
                        <INPUT type="checkbox" name="check_box_line" value=${tot_index}> ${check_box_line} <br>
                        % endfor
                </div>
                <BR>
        % endfor
        
        

         <div id="links">
        
        <INPUT TYPE="hidden" name="new_form_name" VALUE="%s">
        <br><INPUT type="submit"></FORM>

        <br>
        <br>
        <form action='editform' method="get">
        <INPUT TYPE="hidden" name="new_form_name" VALUE="%s">
        <INPUT type='submit' value='Edit form'></form>
       <br>

        % if form_links:
        Links:<br>
        % for link in form_links:
        % if type(link)==dict:
        <% name,url=link.items()[0] %>
        ##<% print url%>

      
        <a href="${url |n}" >${name}</a>
        <br>
        %endif
        % endfor
        <br>
              ##${form_links |u}
        % endif
        </div>
        </div>
        """
        #! http://pathforms.appspot.com/css/test.pdf for rendering
    

class YamlValidator(WebPages,FormEntry,webapp.RequestHandler):
  def __init__(self):
      WebPages.__init__(self)
      FormEntry.__init__(self)
  def failure(self,form_title):
    edit_back="""
    <form action="editform" method="get" accept-charset="utf-8">
      <input type="hidden" name="new_form_name" value="%s">

      <p><input type="submit" value="Continue &rarr;"></p>
    </form>""" %form_title
    try:  
      yaml_form=yaml.load(get_form_content(form_title))
    except:
      return exceptions.html_error_template().render()+edit_back
    try:
      yaml_form=form_translator(yaml_form)
    except:
      return exceptions.html_error_template().render()+edit_back
    # try:
    #     web_publish(self.template.render(yaml_form=yaml_form) %(form_title,form_title))
    # except:
    #   return exceptions.html_error_template().render()+edit_back
      
    return False
      #self.response.out.write(exceptions.html_error_template().render()+edit_back)
    # try:
    #     self.response.out.write(web_publish(self.template.render(yaml_form=yaml_form) %(form_title,form_title)))
    # except:
    #     self.response.out.write(exceptions.html_error_template().render()+edit_back)


def get_form_key(yaml_form):
    if type(yaml_form)==list:
      return yaml_form
    if type(yaml_form)==dict:
      return yaml_form["form"]
      
def get_form_links(yaml_form):
  if type(yaml_form)==dict:
    if yaml_form.has_key("links"):
      return yaml_form["links"]
  else:
    return False
  
      

def form_translator(yaml_form):
    yaml_form=get_form_key(yaml_form)
    yaml_form=[(yaml_form[i],yaml_form[i+1]) for i in range(0,len(yaml_form),2)] 
    #print yaml_form
    return yaml_form
    


class RenderForm(FormEntry,WebPages,webapp.RequestHandler):
    """ Rendering of the unfilled forms,  implementing  class"""
    def __init__(self):
        WebPages.__init__(self)
        FormEntry.__init__(self)
        try:
            self.template=Template(self.forms_template)
            #print self.template.render()
        except:
            self.response.write(exceptions.text_error_template().render())
            #print exceptions.html_error_template().render()
        #self.select=Select()
        
    
    def get(self):
        form_title=cgi.escape(self.request.get('form_title'))
        if YamlValidator().failure(form_title):  #ERROR!!!!
          self.response.out.write(YamlValidator().failure(form_title))
        else:  
          yaml_form=yaml.load(get_form_content(form_title))
          form_links=get_form_links(yaml_form)
          yaml_form=form_translator(yaml_form)
          
          
        #print yaml_form
            #['TEST', ['PCR FOR
                                        #IMMUNOGLOBULIN AND T CELL
                                        #RECEPTOR GENE REARRANGEMENTS
                                        #WAS PERFORMED ON', 'PCR FOR
                                        #IMMUNOGLO

            #[('TEST', ['PCR FOR IMMUNOGLOBULIN\AND T CELL RECEPTOR GENE REARRANGEMENTS WAS PERFORMED ON', 
            #'PCR FOR IMMUNOGLOBULIN AND T
          try:
            self.response.out.write(web_publish(self.template.render(yaml_form=yaml_form,
                                                                  form_links=form_links,
                                                                   disable_unicode=True, 
                                                                   input_encoding='utf-8', 
                                                                  encoding_errors='replace') %(form_title,form_title)))
          except:print get_form_content(form_title)

            

  
class ValidatedEntry(object):
    def __init__(self):
        pass              
   

class RenderSelection(WebPages, webapp.RequestHandler):
    """ ACTUAL RENDERING OF USER SELECTION """
    def __init__(self):
        WebPages.__init__(self)
        self.template_path=localize("forms_results_template.html")
        


    def validate_entry(self,keys):
        """ keys-> 
        Entry.__dict__= {'multiple_choices': [(3, 'HER-2/neu')], 'input_choices': [(3, 'sdfsdf')], 'check_box_lines': [0, 3]}
        """

        Entry=ValidatedEntry()
        if keys.has_key(self.MultipleSelect.get_name):
            multiple_choices=make_list(keys[self.MultipleSelect.get_name])
        else: multiple_choices=[]
        if keys.has_key(self.MultipleSelect.line_index_name):
            multiple_choices_lines=make_list(keys[self.MultipleSelect.line_index_name])
        else: multiple_choices_lines=[]
        Entry.multiple_choices=zip(make_ints(multiple_choices_lines),multiple_choices)

        if keys.has_key(self.Input.get_name):
            text_inputs=make_list(keys[self.Input.get_name])
        else: text_inputs=[]
        if keys.has_key(self.Input.line_index_name):
            input_choices_lines=make_list(keys[self.Input.line_index_name])
        else: input_choices_lines=[]
        Entry.input_choices=zip(make_ints(input_choices_lines),text_inputs)

        if keys.has_key("check_box_line"):
            Entry.check_box_lines= make_ints(make_list(keys["check_box_line"]))
        return Entry
        
        

    def post(self):
        check_box_lines=make_ints(self.request.get("check_box_line", allow_multiple=True))
        multiple_choices=self.request.get("get_multiple_choices", allow_multiple=True)
        line_choices=make_ints(self.request.get("line_index_selection", allow_multiple=True))
        input_entries=self.request.get("get_input_entry", allow_multiple=True)
        line_index_input=make_ints(self.request.get("line_index_imput", allow_multiple=True))
        form_title=self.request.get("new_form_name")
        #print check_box_lines, "CHECKBOXLINES" 
        #print multiple_choices, "MULTIPLE CHOICES" 
        #print line_choices, "LINE CHOICES" 
        #print input_entries, "INPUT ENTRIES"
        #print line_index_input, "LINE INDEX INPUT"
        #print "CHECKBOXLINES"
        Entry=ValidatedEntry()
        Entry.multiple_choices=zip(line_choices, multiple_choices)
        Entry.input_choices=zip(line_index_input, input_entries)
        Entry.check_box_lines=check_box_lines
        #print Entry.__dict__, "YEAH...."
        
        
        #print self.request
        #print self.request.POST.items()
        #print "BEING CALLED"
        
        """keys contains the chosen lines numbers+ a list with all the selected multiple choises"""
         # for debugging
        #yield strope(keys)

        choices=[]
        t=get_form_key(yaml.load(get_form_content(form_title)))
        #t=yaml.load(file(cherrypy.session["fileName"]).read()) #['TEST', ['PCR FOR IMMUNOGLOBULIN AND T CELL RECEPTOR GENE REARRANGEMENTS WAS PERFORMED ON', 'PCR FOR IMMUNOGLO
        [choices.extend(i) for i in (t[i+1] for i in range(0,len(t),2))] # ['HER-2/neu gene', ....
        #yield strope(choices)
        #print choices, "CHOICES"
        
        user = users.get_current_user()
        q = db.GqlQuery("SELECT * FROM Settings WHERE user = :1", user)
        if q.get():
          user_setting=q.get()
          header=user_setting.header
          line_start=user_setting.line_start
        else:
          header=""
          line_start=""
          

        text= header+'<br>'

        index=0
        for chosen_check_box_line_index in Entry.check_box_lines:
            line=choices[chosen_check_box_line_index]+" " 
            #print "RAW", line
           
            for multiple_choice in Entry.multiple_choices: # (14, 'decreased')
                #yield strope(multiple_choice)+strope(chosen_check_box_line_index)
                if multiple_choice[0]==chosen_check_box_line_index and multiple_choice[1]!="default":
                    #continue
                    #yield "CHOICES MATCH"
                    
                    match=self.MultipleSelect.parse(line)
                    if match:
                        match=match[0]
                    #yield strope(match)
                        line=line.replace(match,multiple_choice[1],1)
                if multiple_choice[0]==chosen_check_box_line_index and multiple_choice[1]=="default":
                    #continue
                    #yield "CHOICES MATCH"
                    #yield strope(line)
                    ##print line
                    match=self.MultipleSelect.parse(line)
                    ##print match
                    #yield strope(match)
                    if match:
                    
                        match=match[0]
                        #yield strope(match)
                        line=line.replace(match,"",1)    
            #print "NOT RAW", line                        
            for  input_choice in Entry.input_choices:
                #print input_choice
                
                if input_choice[0]==chosen_check_box_line_index:
                    
                    #yield "INPUT MATCH"
                    match=self.Input.parse(line)[0]
                    #print match, "MATCH", type(match)
                    #print line, type(line), match, type(match), input_choice[1], type(input_choice[1])
                    #continue
                    #yield strope(match)
                    line=line_start+line.replace(match,input_choice[1],1)
                    #continue

            text+=line
            text+="<BR>" 
            # if index==0 or index==1:
            #     #continue
            #     text+="<BR>" 
            index+=1
        #rendering engine
        #print text
      
        #print text, "HERE I AM"
        self.response.out.write(web_publish(template.render(self.template_path,{"form_results":text})))
  



      


application = webapp.WSGIApplication([('/', Select), 
                                      ("/chooseform", ChooseForm ),
                                      ("/saveform", SaveForm),
                                      ("/deleteall",DeleteAll),
                                      ("/renderform", RenderForm),
                                      ("/renderselection", RenderSelection),
                                      ("/editform", EditForm),
                                      ("/setup", SetupPage),
                                      ("/enter_setup",EnterSetup),
                                      ("/emailsender",EmailSender)])
                                      #, 

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
