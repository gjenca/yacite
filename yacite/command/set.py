# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record, Argument
from yacite.exception import *

class Set(YaciteCommand):
    """reads YAML stream, set fieldname to a value.
"""

    name="append"

    arguments=(
        Argument("fieldname",help="Field name."),
        Argument("value",help="A Python expression. This is what fieldname is set to."),
    )

    def execute(self):
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            rec[self.ns.fieldname]=eval(self.ns.value,{})
            print("---")
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        
