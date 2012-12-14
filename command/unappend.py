# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import record_stream,yaml_dump_encoded
from yacite.exception import *

class Unappend(object):


    help="deletes each string in the list from the value of a field"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("fieldname",help="Value of the field must be 'list of strings'.")
        subparser.add_argument("string",nargs="+",help="these strings are removed from the value")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        ustrings=set(s.decode('utf-8') for s in self.ns.string)
        for i,rec in enumerate(record_stream(sys.stdin)):
            if self.ns.fieldname in rec:
                if type(rec[self.ns.fieldname]) is not list:
                    raise DataError("unappend: expecting list under fieldname %s in item %d, got %s instead" %
                        (self.ns.fieldname,i,type(rec[self.ns.fieldname])))
                rec[self.ns.fieldname]=list(set(rec[self.ns.fieldname])-ustrings)
            print "---"
            sys.stdout.write(yaml_dump_encoded(rec))

                
        
        
