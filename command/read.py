# -*- coding: utf-8 -*-

import os,sys
import yaml

from yacite.exception import *

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
                        data=yaml.load(file(path))
                        if type(data) is list:
                            for d in data:
                                print "---"
                                sys.stdout.write(yaml.dump(d,allow_unicode=True))
                        else:
                            print "---"
                            sys.stdout.write(yaml.dump(data,allow_unicode=True))
        else:
            raise NotDirectoryError("%s is not a directory" % ns.datadir) 
        
