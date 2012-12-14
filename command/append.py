# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import record_stream,yaml_dump_encoded
from yacite.utils.misc import describe_item
from yacite.exception import *

class Append(object):


    help="appends each string in the list to the value of a field"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("fieldname",help="Field name. Value must be a 'list of strings'.")
        subparser.add_argument("string",nargs="+",help="these strings are appended to the value")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i,rec in enumerate(record_stream(sys.stdin)):
            if self.ns.fieldname in rec:
                value=rec[self.ns.fieldname]
                if type(value) is not list:
                    raise DataError("append: expecting a list under %s in %s, got %s instead" %
                        (self.ns.fieldname,describe_item(i,rec),type(value)))
                value.extend(self.ns.string)
                value=list(set(value))
                rec[self.ns.fieldname]=value
            else:
                rec[self.ns.fieldname]=[s.decode('utf-8') for s in self.ns.string]
            print "---"
            sys.stdout.write(yaml_dump_encoded(rec))

                
        
        
