# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import record_stream,yaml_dump_encoded
from yacite.exception import *

class Unappend(object):


    help="deletes each string in the list from the value of a variable"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("variable",help="variable. Value of variable must be 'list of strings'.")
        subparser.add_argument("string",nargs="+",help="these strings are removed from the value")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        ustrings=set(s.decode('utf-8') for s in self.ns.string)
        for i,d in enumerate(record_stream(sys.stdin)):
            if self.ns.variable in d:
                if type(d[self.ns.variable]) is not list:
                    raise DataError("unappend: expecting list under variable %s in item %d, got %s instead" %
                        (self.ns.variable,i,type(d[self.ns.variable])))
                d[self.ns.variable]=list(set(d[self.ns.variable])-ustrings)
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
