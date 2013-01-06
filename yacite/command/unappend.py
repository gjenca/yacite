# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.exception import *
from yacite.utils.misc import describe_record

class Unappend(YaciteCommand):


    help="deletes each string in the list from the value of a field"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("fieldname",help="Value of the field must be 'list of strings'.")
        subparser.add_argument("string",nargs="+",help="these strings are removed from the value")


    def execute(self):
        ustrings=set(s.decode('utf-8') for s in self.ns.string)
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            if self.ns.fieldname in rec:
                if type(rec[self.ns.fieldname]) is not list:
                    raise DataError("unappend: expecting list under fieldname %s in %s, got %s instead" %
                        (self.ns.fieldname,describe_record(i,rec),type(rec[self.ns.fieldname])))
                rec[self.ns.fieldname]=list(set(rec[self.ns.fieldname])-ustrings)
            print "---"
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        
