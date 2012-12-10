# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.exception import *

class Append(object):


    help="append a *string* to a list of strings, stored under *name*; for adding a tag"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("name",help="name to add to")
        subparser.add_argument("string",nargs="+",help="strings to append")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i,d in enumerate(docstream(sys.stdin)):
            if self.ns.name in d:
                value=d[self.ns.name]
                if type(value) is not list:
                    raise DataError("append: expecting list under name %s in item %d, got %s instead" %
                        (self.ns.name,i,type(value)))
                value.extend(self.ns.string)
                value=list(set(value))
            else:
                d[self.ns.name]=[s.decode('utf-8') for s in self.ns.string]
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
