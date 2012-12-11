# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_load
from jinja2 import Template,FileSystemLoader,Environment
import pybtex.bibtex.names


def authors_format(authors,bst_format):

    return [pybtex.bibtex.names.format(auth,bst_format) for auth in authors]


class Render(object):


    help="renders records using a jinja2 template"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("-e","--extra-yaml-map",help="additional yaml map to pass to template")
        subparser.add_argument("template",help="template file")

    def __init__(self,ns):
        self.ns=ns
        if ns.extra_yaml_map:
            self.extra_d=yaml_load(ns.extra_yaml_map)
        else:
            self.extra_d={}

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
        env.filters['authorsformat']=authors_format
        t=env.get_template(self.ns.template)
        d={"bibitems":bibitems}
        d.update(self.extra_d)
        sys.stdout.write(t.render(d).encode('utf-8'))

                
        
        
