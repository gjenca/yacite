# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import docstream,yaml_dump_encoded

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
                print >> sys.stderr, "Warning: eval failed on item %d" % i
            else:
                if tf:
                    print "---"
                    sys.stdout.write(yaml_dump_encoded(d))

                
        
        
