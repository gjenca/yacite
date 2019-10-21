# -*- coding: utf-8 -*-

import sys
import yacite.utils.sane_yaml as sane_yaml
from jinja2 import Template,FileSystemLoader,Environment
# pybtex API changed in version 0.20
try:
    from pybtex.bibtex.names import format as format_name
except ImportError:
    from pybtex.bibtex.names import format_name
from yacite.command.command import YaciteCommand
from yacite.utils.compare import keys_to_cmp
from yacite.utils.misc import Argument



def authors_format(authors,bst_format):

    return [format_name(auth,bst_format).replace('~',' ') for auth in authors]

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

    def execute(self):
        records=list(sane_yaml.load_all(sys.stdin))
        key_dict={}
        edge_tags={}
        records_new=[]
        for rec in records:
            if "key" in rec:
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
            cites_objects=[]
            for key in rec["cites"]:
                if ';' in key:
                    key,tags_s=key.split(';')
                    tags=tags_s.split(' ')
                    edge_tags[(rec["key"],key)]=tags
                if key not in key_dict:
                    continue
                cites_objects.append(key_dict[key])
            rec["cites"]=cites_objects
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
        sys.stdout.write(t.render(citation_tags=edge_tags,records=records,extra=self.extra))




