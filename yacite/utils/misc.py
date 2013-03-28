# -*- coding: utf-8 -*-

import unicodedata

def describe_record(i,rec):
    
    return "record no. %d (key=%s)" % (i,rec.get("key","None")) 

def strip_accents(s):

    return unicodedata.normalize('NFKD',s).encode("ascii","ignore").decode("ascii")

