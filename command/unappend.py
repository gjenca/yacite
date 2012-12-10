# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.exception import *

class Unappend(object):


    help="delete a *string* to a list of strings, stored under *name*; for removing a tag"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("name",help="name to remove the string from")
        subparser.add_argument("string",nargs="+",help="strings to remove")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        ustrings=set(s.decode('utf-8') for s in self.ns.string)
        for i,d in enumerate(docstream(sys.stdin)):
            if self.ns.name in d:
                if type(d[self.ns.name]) is not list:
                    raise DataError("unappend: expecting list under name %s in item %d, got %s instead" %
                        (self.ns.name,i,type(d[self.ns.name])))
                d[self.ns.name]=list(set(d[self.ns.name])-ustrings)
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
