# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.exception import *

class Unappend(object):


    help="delete a *string* to a list of strings, stored under *name*; for removing a tag"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("name",help="name to remove the string from")
        subparser.add_argument("string",help="string to remove")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        ustring=self.ns.string.encode('utf-8')
        for i,d in enumerate(docstream(sys.stdin)):
            if self.ns.name in d:
                value=d[self.ns.name]
                if type(value) is not list:
                    raise DataError("unappend: expecting list under name %s in item %d, got %s instead" %
                        (self.ns.name,i,type(value)))
                if ustring in value:
                    value.remove(ustring)
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
