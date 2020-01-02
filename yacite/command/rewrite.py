# -*- coding: utf-8 -*-

import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.exception import *
from yacite.utils.misc import describe_record, Argument
import re
from yacite.command.command import YaciteCommand

class Rewrite(YaciteCommand):
    """reads YAML stream, rewrites values of a given field using a file with rewrite rules,outputs YAML stream
"""

    name="rewrite"
    
    arguments=(
        Argument("fieldname",help="field name"),
        Argument("rewrite_file",help="file with rewrite rules - see the docs for format"),
    )

    def __init__(self,ns):
        self.ns=ns
        rf=sane_yaml.load(open(ns.rewrite_file))
        if type(rf) is not list:
            raise DataError("rewrite: file %s should contain list of pairs of strings" % ns.rewrite_file)
        self.rules=[]
        for rule in rf:
            if type(rule) is not list or len(rule)!=2:
                raise DataError("rewrite: file %s should contain list of pairs of strings" % ns.rewrite_file)
            head,tail=rule
            if type(head) not in (str,str) or type(tail) not in (str,str):
                raise DataError("rewrite: file %s should contain list of pairs of strings" % ns.rewrite_file)
            self.rules.append((re.compile(head),tail))

    def execute(self):
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            if self.ns.fieldname in rec:
                if type(rec[self.ns.fieldname]) in (str,str):
                    for pat,repl_with in self.rules: 
                        rec[self.ns.fieldname]=pat.sub(repl_with,rec[self.ns.fieldname])
                elif type(rec[self.ns.fieldname]) is not list:
                    raise DataError("rewrite: %s in %s is %s, expected a string or list" % 
                        (self.ns.fieldname,describe_record(i,rec),type(rec[self.ns.fieldname])))
                for pat,repl_with in self.rules:
                    new=[]
                    for s in rec[self.ns.fieldname]:
                        new.append(pat.sub(repl_with,s))
                    rec[self.ns.fieldname]=new
            print("---")
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        
