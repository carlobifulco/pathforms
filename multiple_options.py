#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2006-2008 Carlo Bifulco
# See LICENSE for details.



import re
from mako.template import Template
from  doctest import testmod
#import doctest.testmod


class AbstractMatcher(object):
    """docstring for AbstractMatcher"""
    def __init__(self):
        pass
        
    def parse(self,text_line):
        matches=False
        #print text_line
        matches=self.PATTERN.findall(text_line) # -> [match1,match2 ....]
        if matches:
            return matches
        else:
            return False    
            
    def parse_and_render(self,text,index):
        matches=self.parse(text)
        if matches: 
            for to_be_replaced in matches:
                text=text.replace(to_be_replaced,self.render(to_be_replaced,index))
        return text
            
    def render(self,text_options,index):
        "To be implemented"
        pass


class MultipleSelect(AbstractMatcher):
    def __init__(self):
        self.line_index_name="line_index_selection"
        AbstractMatcher.__init__(self)
        self.PATTERN =re.compile(r"\[.*?\]") #? makes .* non-greedy
        self.get_name="get_multiple_choices"
        self.form=Template("""
        <select  name=${get_name}>
        <option value="default"> </option>
        % for option in options:
         <option value="${option}">${option}</option>
        % endfor     
        </select>
        <INPUT TYPE="hidden" name="${line_index_name}" VALUE=${index}>
        """)
    def render(self,text_options,index):

        text_options=text_options.replace("[","")
        text_options=text_options.replace("]","")
        text_options=text_options.split("|")

        return self.form.render(get_name=self.get_name,options=text_options,\
            index=index,line_index_name=self.line_index_name).strip()
    
    
class Input(AbstractMatcher):
    def __init__(self):
        AbstractMatcher.__init__(self)
        self.line_index_name="line_index_imput"
        self.PATTERN=re.compile(r"\$")
        self.get_name="get_input_entry"
        self.form=Template("""<input type="text" name=${get_name} 
        value=""  id="some_name"> <INPUT TYPE="hidden" 
        NAME="${line_index_name}" VALUE="${index_line}"> </input>""")
        
    def render(self,select,index_line):
        return  self.form.render(get_name=self.get_name,index_line=index_line,\
            line_index_name=self.line_index_name)
        
    



    

    






def _test():
    import doctest
    doctest.testmod(verbose=True)

if __name__ == "__main__":
    _test()    
