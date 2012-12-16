# -*- coding: utf-8 -*-

import sys
import yacite.utils.sane_yaml as sane_yaml
from jinja2 import Template,FileSystemLoader,Environment
import pybtex.bibtex.names


def authors_format(authors,bst_format):

    return [pybtex.bibtex.names.format(auth,bst_format) for auth in authors]


class Render(object):


    help="renders records using a jinja2 template"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("-e","--extra-yaml",help="additional yaml to pass to template")
        subparser.add_argument("template",help="template file")

    def __init__(self,ns):
        self.ns=ns
        if ns.extra_yaml:
            self.extra=yaml_load(ns.extra_yaml)
        else:
            self.extra=None

    def execute(self):
        records=list(sane_yaml.load_all(sys.stdin))
        key_dict={}
        for rec in records:
            if "key" in rec:
                key_dict[rec["key"]]=rec
        for rec in records:
            if "myown" not in rec:
                rec["myown"]=False
            if not "citedby" in rec:
                rec["citedby"]=[]
            if not "cites" in rec:
                rec["cites"]=[]
            rec["cites"]=[key_dict[key] for key in rec["cites"] if key in key_dict]
        for rec in records:
            if "arxiv" in rec:
                rec["arxivurl"]="http://arxiv.org/abs/%s" % rec["arxiv"]
        for rec in records:
            if rec["myown"]:
                continue
            for cited in rec["cites"]:
                cited["citedby"].append(rec)
        env=Environment(loader=FileSystemLoader('templates'),
            line_statement_prefix="#")
        env.filters['authorsformat']=authors_format
        t=env.get_template(self.ns.template)
        sys.stdout.write(t.render(records=records,extra=self.extra).encode('utf-8'))

                
        
        
