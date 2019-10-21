# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record, Argument
from yacite.exception import *

class Append(YaciteCommand):
    """reads YAML stream, appends all strings in the list to the value of a field, outputs YAML stream
"""

    name="append"

    arguments=(
        Argument("fieldname",help="Field name. Value must be a 'list of strings', if it does exist. If it does not, it is created."),
        Argument("string",nargs="+",help="these strings are appended to the value"),
    )

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
                rec[self.ns.fieldname]=[s for s in self.ns.string]
            print("---")
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        
