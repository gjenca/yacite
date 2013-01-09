# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record 

class Filter(YaciteCommand):


    help="evaluates a python expression in the context of the each record, outputs records for which expression returns True"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("--myown",
            action='store_true',
            help="filter applies only if myown == True, otherwise the record passes through")
        subparser.add_argument("--notmyown",
            action='store_true',
            help="filter applies only if myown == False or undefined, otherwise the record passes through")
        subparser.add_argument("expr",help="python expression")
        subparser.add_argument("-f","--failed",action="store_true",help="output only the failed records,supress error message")
        subparser.add_argument("-k","--keep-going",action="store_true",help="do not stop when the eval(expr) throws an exception")


    def execute(self):
        exceptions=0
        for i,rec in enumerate(sane_yaml.load_all(sys.stdin)):
            if self.ns.myown:
                if (not u"myown" in rec) or rec[u"myown"]==False:
                    print "---"
                    sys.stdout.write(sane_yaml.dump(rec))
                    continue
            if self.ns.notmyown:
                if "myown" in rec and rec[u"myown"]:
                    print "---"
                    sys.stdout.write(sane_yaml.dump(rec))
                    continue
            try:
                tf=eval(self.ns.expr,dict(rec))
            except:
                if self.ns.failed:
                    if '__builtins__' in rec:    
                        del rec['__builtins__']
                    print "---"
                    sys.stdout.write(sane_yaml.dump(rec))
                elif self.ns.keep_going:
                    exceptions+=1
                    print >> sys.stderr, "filter: Warning: failed on %s" % describe_record(i,rec)
                    print >> sys.stderr, "filter: The exception was %s" % sys.exc_info()[0]
                else:
                    raise
            else:
                if not self.ns.failed and tf:
                    print "---"
                    sys.stdout.write(sane_yaml.dump(rec))

        if exceptions and not self.ns.failed:
            print >> sys.stderr, "exec: Warning: there were %d exceptions" % exceptions
            
        
        