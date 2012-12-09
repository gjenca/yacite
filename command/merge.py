# -*- coding: utf-8 -*-

import sys

from yacite.types import Datadir
from yacite.exception import *
from yacite.types import BibObject
from yacite.utils.docstream import docstream


class Merge(object):


    help="merge docstream from stdin with datadir"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")

    def __init__(self,ns):
        self.datadir_name=ns.datadir
        self.datadir=Datadir(self.datadir_name)

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
                    if key in match:
                        if type(d[key]) is list:
                            if type(match[key]) is list:
                                match[key].extend(d[key])
                                match[key]=list(set(match[key]))
                            else:
                                raise DataError(
                                    "merge: Type conflict: item %d in stream, file='%s', key='%s"
                                    % (i,match.path,key))
                        elif type(match[key]) is list:
                            raise DataError(
                                "merge: Type conflict: item %d in stream, file='%s', key='%s"
                                % (i,match.path,key))
                        else:
                            match[key]=d[key]
                    else:
                        match[key]=d[key]
                match.save()
            else:
                newitem=BibObject(d,datadir=self.datadir)
                newitem.dirty=True
                newitem.save()
                self.datadir.append(newitem)



                            
                


        
        
