# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded,yaml_load
from yacite.exception import *
import re

class Rewrite(object):


    help="rewrite values of *variable* using *rewrite_file*"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("variable",help="variable")
        subparser.add_argument("rewrite_file",help="file with rewrite rules")

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
        for i,d in enumerate(docstream(sys.stdin)):
            if self.ns.variable in d:
                if type(d[self.ns.variable]) in (str,unicode):
                    for pat,repl_with in self.rules: 
                        d[self.ns.variable]=pat.sub(repl_with,d[self.ns.variable])
                elif type(d[self.ns.variable]) is not list:
                    raise DataError("rewrite: %s in item %d is %s, expected a string or list" % 
                        (self.ns.variable,i,type(d[self.ns.variable])))
                for pat,repl_with in self.rules:
                    new=[]
                    for s in d[self.ns.variable]:
                        new.append(pat.sub(repl_with,s))
                    d[self.ns.variable]=new
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
