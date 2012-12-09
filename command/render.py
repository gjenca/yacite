# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream
from jinja2 import Template,FileSystemLoader,Environment

class Render(object):


    help="render input stream using a jinja2 template"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("template",help="template file")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        bibitems=list(docstream(sys.stdin))
        keybi={}
        for bi in bibitems:
            if "key" in bi:
                keybi[bi["key"]]=bi
        for bi in bibitems:
            if "myown" not in bi:
                bi["myown"]=False
            if not "citedby" in bi:
                bi["citedby"]=[]
            if not "cites" in bi:
                bi["cites"]=[]
            bi["cites"]=[keybi[key] for key in bi["cites"] if key in keybi]
        for bi in bibitems:
            if "arxiv" in bi:
                bi["arxivurl"]="http://arxiv.org/abs/%s" % bi["arxiv"]
        for bi in bibitems:
            if bi["myown"]:
                continue
            for cited in bi["cites"]:
                cited["citedby"].append(bi)
        env=Environment(loader=FileSystemLoader('templates'),
            line_statement_prefix="#")
        t=env.get_template(self.ns.template)
        sys.stdout.write(t.render(bibitems=bibitems).encode('utf-8'))

                
        
        
