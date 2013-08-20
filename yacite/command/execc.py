# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record, Argument, MexGroup

class Exec(YaciteCommand):
    """execute a python statement on every record
"""
    arguments=(
        Argument("statement",help="python statement"),
        MexGroup(
            Argument("-n","--no-output",action="store_true",help="supress normal yaml output stream; any intended output must be preformed by statement itself"),
            Argument("-f","--failed",action="store_true",help="output only the failed records,supress error messages")),
        Argument("-k","--keep-going",action="store_true",help="do not stop when the statement throws an exception"),
        Argument("-m","--module",action="append",default=[],help="python module to import; multiple -m options are possible")
    )
    
    def __init__(self,ns):
        
        super(Exec,self).__init__(ns)
        self.mods={}
        for m in self.ns.module:
            self.mods[m]=__import__(m)


    def execute(self):
        exceptions=0
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            try:
                exec self.ns.statement in self.mods,rec
            except:
                if self.ns.failed:
                    print "---"
                    sys.stdout.write(sane_yaml.dump(rec))
                elif self.ns.keep_going:
                    exceptions+=1
                    print >> sys.stderr, "exec: Warning: failed on %s" % describe_record(i,rec)
                    print >> sys.stderr, "exec: The exception was %s" % sys.exc_info()[0]
                else:
                    raise
            if not self.ns.no_output and not self.ns.failed:
                print "---"
                sys.stdout.write(sane_yaml.dump(rec))
        if exceptions and not self.ns.failed:
            print >> sys.stderr, "exec: Warning: there were %d exceptions" % exceptions
            

                
        
        
