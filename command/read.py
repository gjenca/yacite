# -*- coding: utf-8 -*-

import os,sys

from yacite.exception import *
from yacite.utils.sane_yaml import yaml_load_as_unicode,yaml_dump_encoded

class Read(object):


    help="read datadir"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        if os.path.isdir(self.ns.datadir):
            for root,dirs,files in os.walk(self.ns.datadir):
                for name in files:
                    if name.endswith(".yaml"):
                        path=os.path.join(root,name)
                        data=yaml_load_as_unicode(file(path))
                        if type(data) is list:
                            for d in data:
                                print "---"
                                sys.stdout.write(yaml_dump_encoded(d))
                        else:
                            print "---"
                            sys.stdout.write(yaml_dump_encoded(data))
        else:
            raise NotDirectoryError("%s is not a directory" % ns.datadir) 
        
