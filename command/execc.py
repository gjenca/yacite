# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.utils.misc import describe_item 

class Exec(object):


    help="execute a python statement on every record"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("statement",help="python statement")
        group=subparser.add_mutually_exclusive_group()
        group.add_argument("-q","--quiet",action="store_true",help="supress output stream")
        subparser.add_argument("-k","--keep-going",action="store_true",help="do not stop when the statement throws an exception")
        group.add_argument("-f","--failed",action="store_true",help="output only the failed records,supress error message")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        exceptions=0
        for i,d in enumerate(docstream(sys.stdin)):
            try:
                exec self.ns.statement in d
            except:
                if self.ns.failed:
                    if '__builtins__' in d:    
                        del d['__builtins__']
                    print "---"
                    sys.stdout.write(yaml_dump_encoded(d))
                elif self.ns.keep_going:
                    exceptions+=1
                    print >> sys.stderr, "exec: Warning: failed on item %s" % describe_item(i,d)
                    print >> sys.stderr, "exec: The exception was %s" % sys.exc_info()[0]
                else:
                    raise
            if '__builtins__' in d:    
                del d['__builtins__']
            if not self.ns.quiet and not self.ns.failed:
                print "---"
                sys.stdout.write(yaml_dump_encoded(d))
        if exceptions and not self.ns.failed:
            print >> sys.stderr, "exec: Warning: there were %d exceptions" % exceptions
            

                
        
        
