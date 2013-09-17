# -*- coding: utf-8 -*-

import unicodedata

def describe_record(i,rec):
    
    return "record no. %d (key=%s)" % (i,rec.get("key","None")) 

def strip_accents(s):

    return unicodedata.normalize('NFKD',s).encode("ascii","ignore").decode("ascii")

class Argument(object):

    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs


class MexGroup(object):

    def __init__(self,*args):
        self.arguments=tuple(args)
