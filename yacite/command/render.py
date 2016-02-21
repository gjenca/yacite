# -*- coding: utf-8 -*-

import sys
import yacite.utils.sane_yaml as sane_yaml
from jinja2 import Template,FileSystemLoader,Environment
import pybtex.bibtex.names
from yacite.command.command import YaciteCommand
from yacite.utils.compare import keys_to_cmp
from yacite.utils.misc import Argument

def authors_format(authors,bst_format):

    return [pybtex.bibtex.names.format(auth,bst_format) for auth in authors]

def merge(dest,src):

    for k in src:
        if k not in dest:
            dest[k]=src
        else:
            if type(dest[k]) is list and type(src[k]) is list:
                dest[k].extend(src[k])
                dest[k]=list(set(dest[k]))

class Render(YaciteCommand):
    """reads YAML stream, renders records using a jinja2 template, outputs YAML stream
"""

    does_output = True

    name="render"
    
    arguments=(
        Argument("-e","--extra-yaml",help="additional yaml to pass to template; the data is available as `extra` "),
        Argument("-k","--sort-key",action="append",help="either fieldname of ~fieldname (for citedby sorting)"),
        Argument("-t","--template-dir",default="./templates",help="directory with templates; default: ./templates"),
        Argument("template",help="template file"),
    )

    def __init__(self,ns):
        self.ns=ns
        if ns.extra_yaml:
            self.extra=sane_yaml.load(ns.extra_yaml)
        else:
            self.extra=None
        if self.ns.sort_key:
            self.cmp_keys=keys_to_cmp(self.ns.sort_key)
        else:
            self.cmp_keys=None

    def execute(self,iter_in):
        records=list(iter_in)
        key_dict={}
        records_new=[]
        for rec in records:
            if "key" in rec:
                if "@" in rec["key"]:
                    key_main=rec["key"][:rec["key"].find("@")]
                    if key_main in key_dict:
                        # Twin records are merged
                        rec["key"]=key_main
                        merge(key_dict[key_main],rec)
                        # the other twin is not appended
                        continue
                    else:
                        rec["key"]=key_main
                key_dict[rec["key"]]=rec
            records_new.append(rec)
        records=records_new
        for rec in records:
            if "myown" not in rec:
                rec["myown"]=False
            if not "citedby" in rec:
                rec["citedby"]=[]
            if not "cites" in rec:
                rec["cites"]=[]
            rec["cites"]=[key_dict[key] for key in rec["cites"] if key in key_dict]
            rec["cited_times"]=0
        for rec in records:
            if rec["myown"]:
                continue
            for cited in rec["cites"]:
                cited["cited_times"]+=1
                cited["citedby"].append(rec)
        if self.cmp_keys:
            for rec in records:
                rec["citedby"].sort(cmp=self.cmp_keys)
        env=Environment(loader=FileSystemLoader(self.ns.template_dir),
            line_statement_prefix="#")
        env.filters['authorsformat']=authors_format
        t=env.get_template(self.ns.template)
        sys.stdout.write(t.render(records=records,extra=self.extra).encode('utf-8'))

                
        
        
