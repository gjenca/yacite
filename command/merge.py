# -*- coding: utf-8 -*-

import sys

from yacite.types import Datadir
from yacite.exception import *
from yacite.types import BibObject
from yacite.utils.sane_yaml import docstream


class Merge(object):


    help="merge records with datadir - see the docs for merge rules"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")
        subparser.add_argument("-u","--union",help="take union of lists - original and new",
            dest="uname",action="append",default=[])
        subparser.add_argument("-s","--set",help="replace orginal values by new value",
            dest="sname",action="append",default=[])
        subparser.add_argument("-d","--delete-names",help="delete fields",dest="dname",action="append",
            default=[])

    def __init__(self,ns):
        self.datadir_name=ns.datadir
        self.datadir=Datadir(self.datadir_name)
        self.union_names=ns.uname
        self.set_names=ns.sname
        self.delete_names=ns.dname
        if "ALL" in self.set_names and \
            (self.union_names,self.set_names,self.delete_names) != ([],["ALL"],[]):
            raise ParameterError("merge: --set ALL must be the only option")

    def execute(self):

        for i,d in enumerate(docstream(sys.stdin)):
            if type(d) is not dict:
                raise DataError("merge: Expecting dict as item %d in stream, got %s instead" % (i,type(d)))
            matches=self.datadir.list_matching(d)
            if len(matches)>1:
                raise DataError("merge: Item %d in stream matches multiple items in datadir" % i)
            elif len(matches)==1:
                match=matches[0]
                for key in d:
                    if (key in self.set_names) or (key not in match):
                         match[key]=d[key]
                         continue
                    elif (key in self.union_names) and (key in match):
                        if type(d[key]) is list and type(match[key]) is list:
                            match[key].extend(d[key])
                            match[key]=list(set(match[key]))
                            continue
                        else:
                            raise DataError(
                             "merge: union of non-lists requested: item %d in stream, file='%s', key='%s"
                                % (i,match.path,key))
                    elif key in self.delete_names and key in match:
                        del match[key]
                        match.dirty=True
                match.save()
            else:
                newitem=BibObject(d,datadir=self.datadir)
                newitem.dirty=True
                newitem.save()
                self.datadir.append(newitem)
        
