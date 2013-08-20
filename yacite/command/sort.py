# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.exception import *
from yacite.utils.compare import keys_to_cmp
from yacite.utils.misc import Argument

class Sort(YaciteCommand):
    "sorts the records in input stream according to given fields"
    
    arguments=(
        Argument("-k","--sort-key",action="append",help="either fieldname of ~fieldname"),
    )

    def __init__(self,ns):
        self.ns=ns

        if not self.ns.sort_key:
            raise ParameterError("sort: no key(s) given")

        self.cmp_keys=keys_to_cmp(self.ns.sort_key)

    def execute(self):

        l=list(sane_yaml.load_all(sys.stdin))
        l.sort(cmp=self.cmp_keys)
        for d in l:
            print "---"
            sys.stdout.write(sane_yaml.dump(d))

                
        
        
