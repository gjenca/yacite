# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.exception import *

class Append(object):


    help="appends each string in the list to the value of a variable"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("variable",help="variable. Value of variable must be 'list of strings'.")
        subparser.add_argument("string",nargs="+",help="these strings are appended to the value")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i,d in enumerate(docstream(sys.stdin)):
            if self.ns.variable in d:
                value=d[self.ns.variable]
                if type(value) is not list:
                    raise DataError("append: expecting list under variable %s in item %d, got %s instead" %
                        (self.ns.variable,i,type(value)))
                value.extend(self.ns.string)
                value=list(set(value))
                d[self.ns.variable]=value
            else:
                d[self.ns.variable]=[s.decode('utf-8') for s in self.ns.string]
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
