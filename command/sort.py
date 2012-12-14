# -*- coding: utf-8 -*-

import sys
from yacite.utils.sane_yaml import record_stream,yaml_dump_encoded
from yacite.exception import *

class Sort(object):


    help="sorts the items in input stream"

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

        l=list(record_stream(sys.stdin))
        l.sort(cmp=self.cmp_keys)
        for d in l:
            print "---"
            sys.stdout.write(yaml_dump_encoded(d))

                
        
        
