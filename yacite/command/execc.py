# -*- coding: utf-8 -*-

import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record 

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
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            try:
                exec self.ns.statement in rec
            except:
                if self.ns.failed:
                    if '__builtins__' in rec:    
                        del rec['__builtins__']
                    print "---"
                    sys.stdout.write(sane_yaml.dump(rec))
                elif self.ns.keep_going:
                    exceptions+=1
                    print >> sys.stderr, "exec: Warning: failed on %s" % describe_record(i,rec)
                    print >> sys.stderr, "exec: The exception was %s" % sys.exc_info()[0]
                else:
                    raise
            if '__builtins__' in rec:    
                del rec['__builtins__']
            if not self.ns.quiet and not self.ns.failed:
                print "---"
                sys.stdout.write(sane_yaml.dump(rec))
        if exceptions and not self.ns.failed:
            print >> sys.stderr, "exec: Warning: there were %d exceptions" % exceptions
            

                
        
        
