# -*- coding: utf-8 -*-

class YaciteCommand(object):

    def __init__(self,ns):
        self.ns=ns
                
    @classmethod
    def add_arguments(cls,subparser):
        for arg in arguments:
            subparser.add_argument(*arg.args,**arg.kwargs)

        
        
