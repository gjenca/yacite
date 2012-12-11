# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.utils.misc import describe_item 

class Exec(object):


    help="execute a python statement on every record"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("statement",help="python statement")
        subparser.add_argument("-q","--quiet",action="store_true",help="supress output stream")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i,d in enumerate(docstream(sys.stdin)):
            try:
                exec self.ns.statement in d
            except:
                print >> sys.stderr, "exec: Warning: failed on item %s" % describe_item(i,d)
#                print >> sys.stderr, sys.exc_info[0]
            if '__builtins__' in d:    
                del d['__builtins__']
            if not self.ns.quiet:
                print "---"
                sys.stdout.write(yaml_dump_encoded(d))

                
        
        
