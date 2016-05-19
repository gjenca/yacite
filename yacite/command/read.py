# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import os,sys

from yacite.exception import *
from yacite.types import Datadir
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import Argument, MexGroup

class Read(YaciteCommand):
    """reads records from datadir, outputs them as a YAML stream
"""

    name="read"
    
    arguments=(
        Argument("datadir",help="data directory"),
    )

    does_input=True

    def execute(self,iter_in=None):
        dd=Datadir(self.ns.datadir)
        for rec in dd:
            yield dict(rec)
        
