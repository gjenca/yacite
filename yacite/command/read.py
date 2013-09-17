# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import os,sys

from yacite.exception import *
from yacite.types import Datadir
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import Argument, MexGroup

class Read(YaciteCommand):
    """reads records from datadir, outputs them
"""

    name="read"
    
    arguments=(
        Argument("datadir",help="data directory"),
    )


    def execute(self):
        dd=Datadir(self.ns.datadir)
        for rec in dd:
            print "---"
            sys.stdout.write(sane_yaml.dump(dict(rec)))
        
