# -*- coding: utf-8 -*-

import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.exception import *
from yacite.utils.misc import describe_record
import re
from yacite.command.command import YaciteCommand

class Rewrite(YaciteCommand):


    help="rewrites values of a given field using a file with rewrite rules"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("fieldname",help="field name")
        subparser.add_argument("rewrite_file",help="file with rewrite rules - see the docs for format")

    def __init__(self,ns):
        self.ns=ns
        f=file(ns.rewrite_file)
        rf=yaml_load(f)
        if type(rf) is not list:
            raise DataError("rewrite: file %s should contain list of pairs of strings" % ns.rewrite_file)
        self.rules=[]
        for rule in rf:
            if type(rule) is not list or len(rule)!=2:
                raise DataError("rewrite: file %s should contain list of pairs of strings" % ns.rewrite_file)
            head,tail=rule
            if type(head) not in (str,unicode) or type(tail) not in (str,unicode):
                raise DataError("rewrite: file %s should contain list of pairs of strings" % ns.rewrite_file)
            self.rules.append((re.compile(head),tail))

    def execute(self):
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            if self.ns.fieldname in rec:
                if type(rec[self.ns.fieldname]) in (str,unicode):
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
            print "---"
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        