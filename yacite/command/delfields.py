# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record,Argument
from yacite.exception import *

class DelFields(YaciteCommand):
    "reads YAML stream, deletes some fields, writes YAML stream"

    name="delfields"

    arguments=(
        Argument("fieldname",nargs="+",help="fields to delete"),
    )

    def execute(self):
        for rec in sane_yaml.load_all(sys.stdin):
            for fn in self.ns.fieldname:
                if fn in rec:
                    del rec[fn]
            print "---"
            sys.stdout.write(sane_yaml.dump(rec))

                
        
        
