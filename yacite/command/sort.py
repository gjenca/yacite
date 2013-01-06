# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.exception import *

class Sort(YaciteCommand):


    help="sorts the records in input stream according to given fields"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("-k","--sort-key",action="append",help="either fieldname of ~fieldname")

    def __init__(self,ns):
        self.ns=ns

        if not self.ns.sort_key:
            raise ParameterError("sort: no keys given")

        sgn_fieldnames=[]
        for k in self.ns.sort_key:
            if k[0]=="~":
                sgn_fieldnames.append((-1,k[1:]))
            else:
                sgn_fieldnames.append((1,k))
        
        def cmp_keys(d1,d2):
            
            for sgn,fieldname in sgn_fieldnames:
                c=cmp(d1[fieldname],d2[fieldname])*sgn
                if c:
                    return c
            return 0

        self.cmp_keys=cmp_keys

    def execute(self):

        l=list(sane_yaml.load_all(sys.stdin))
        l.sort(cmp=self.cmp_keys)
        for d in l:
            print "---"
            sys.stdout.write(sane_yaml.dump(d))

                
        
        
