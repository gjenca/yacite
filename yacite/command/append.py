# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record
from yacite.exception import *

class Append(YaciteCommand):


    help="appends all strings in the list to the value of a field"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("fieldname",help="Field name. Value must be a 'list of strings'.")
        subparser.add_argument("string",nargs="+",help="these strings are appended to the value")


    def execute(self):
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            if self.ns.fieldname in rec:
                value=rec[self.ns.fieldname]
                if type(value) is not list:
                    raise DataError("append: expecting a list under %s in %s, got %s instead" %
                        (self.ns.fieldname,describe_record(i,rec),type(value)))
                value.extend(self.ns.string)
                value=list(set(value))
                rec[self.ns.fieldname]=value
            else:
                rec[self.ns.fieldname]=[s.decode('utf-8') for s in self.ns.string]
            print "---"
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        
