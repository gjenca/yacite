# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import os,sys

from yacite.exception import *
from yacite.types import Datadir
import yacite.utils.sane_yaml as sane_yaml

class Read(YaciteCommand):


    help="reads records from datadir, outputs them"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")


    def execute(self):
        dd=Datadir(self.ns.datadir)
        for rec in dd:
            print "---"
            sys.stdout.write(sane_yaml.dump(dict(rec)))
        
