# -*- coding: utf-8 -*-

from yacite.command.command import YaciteCommand
import sys
import yacite.utils.sane_yaml as sane_yaml
from yacite.utils.misc import describe_record,strip_accents,Argument
from yacite.exception import *
from yacite.types import BibRecord
import difflib

def isjunk(s):
    return s.isspace()

def strongly_similar(rec1,rec2,field_name):

    if field_name not in rec1 or field_name not in rec2:
        return False
    if field_name == "authors":
        return rec2.same_authors(rec1,preprocess=strip_accents)
    elif all(t in (unicode,str) for t in (type(rec1[field_name]),type(rec2[field_name]))):
        ratio=difflib.SequenceMatcher(isjunk,rec1[field_name],rec2[field_name]).ratio()
        return ratio>0.85
    elif type(rec1[field_name]) is list and type(rec2[field_name]) is list:
        return set(rec1[field_name])==set(rec2[field_name])
    else:
        return rec1[field_name]==rec2[field_name]
        

class CheckDups(YaciteCommand):
    "reads YAML stream, checks for duplicities, writes list of pairs of keys to stdout"
    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("fieldname",nargs="+",help="fields to check for similarities")


    def execute(self):
        everything=[BibRecord(d) for d in sane_yaml.load_all(sys.stdin)]
        if any("key" not in rec for rec in everything):
            print >>sys.stderr,"checkdups: All records MUST have a key field"
        dupkeys=[]
        for rec1 in everything:
            for rec2 in everything:
                if rec1["key"]<=rec2["key"]:
                    continue
                if all(strongly_similar(rec1,rec2,fn) for fn in self.ns.fieldname):
                    dupkeys.append([rec1["key"],rec2["key"]])
        sys.stdout.write(sane_yaml.dump(dupkeys))
                
        
        
