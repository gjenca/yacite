# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded
from yacite.utils.misc import describe_item 

class Filter(object):


    help="evaluates a python expression in the context of the each record, outputs records for which expression returns True"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("--myown",
            action='store_true',
            help="filter applies only is myown == True, otherwise the record passes through")
        subparser.add_argument("--notmyown",
            action='store_true',
            help="filter applies only is myown == False or undefined, otherwise the record passes through")
        subparser.add_argument("expr",help="python expression")
        subparser.add_argument("-f","--failed",action="store_true",help="output only the failed records,supress error message")

    def __init__(self,ns):
        self.ns=ns

    def execute(self):
        for i,d in enumerate(docstream(sys.stdin)):
            if self.ns.myown:
                if (not u"myown" in d) or d[u"myown"]==False:
                    print "---"
                    sys.stdout.write(yaml_dump_encoded(d))
                    continue
            if self.ns.notmyown:
                if "myown" in d and d[u"myown"]:
                    print "---"
                    sys.stdout.write(yaml_dump_encoded(d))
                    continue
            try:
                tf=eval(self.ns.expr,dict(d))
            except:
                if self.ns.failed:
                    if '__builtins__' in d:    
                        del d['__builtins__']
                    print "---"
                    sys.stdout.write(yaml_dump_encoded(d))
                else:
                    print >> sys.stderr, "exec: Warning: failed on item %s" % describe_item(i,d)
                    print >> sys.stderr, "exec: The exception was %s" % sys.exc_info()[0]
            else:
                if not self.ns.failed and tf:
                    print "---"
                    sys.stdout.write(yaml_dump_encoded(d))

                
        
        
