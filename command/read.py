# -*- coding: utf-8 -*-

import os,sys

from yacite.exception import *
from yacite.types import Datadir
from yacite.utils.sane_yaml import yaml_load_as_unicode,yaml_dump_encoded

class Read(object):


    help="reads records from datadir, outputs them"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        dd=Datadir(self.ns.datadir)
        for rec in dd:
            print "---"
            sys.stdout.write(yaml_dump_encoded(dict(rec)))
        
