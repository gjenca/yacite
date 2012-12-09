# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded

class Exec(object):


    help="execute a python statement on every item in input stream"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("statement",help="python statement")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i,d in enumerate(docstream(sys.stdin)):
            try:
                exec self.ns.statement in d
            except:
                print >> sys.stderr, "exec: Warning: exec failed on item %d" % i
            if '__builtins__' in d:    
                del d['__builtins__']
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
