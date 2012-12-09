# -*- coding: utf-8 -*-

import sys

from yacite.types import Datadir
from yacite.exception import *
from yacite.types import BibObject
from yacite.utils.sane_yaml import docstream


class Replace(object):


    help="replace items in datadir by matchin items from docstream"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")

    def __init__(self,ns):
        self.datadir_name=ns.datadir
        self.datadir=Datadir(self.datadir_name)

    def execute(self):

        for i,d in enumerate(docstream(sys.stdin)):
            if type(d) is not dict:
                raise DataError("replace: Expecting dict as item %d in stream, got %s instead" % (i,type(d)))
            matches=self.datadir.list_matching(d)
            if len(matches)>1:
                raise DataError("replace: Item %d in stream matches multiple items in datadir" % i)
            elif len(matches)==1:
                match=matches[0]
                match.update(d)
                match.dirty=True
                match.save()
            else:
                raise DataError("replace: Item %d in stream matches no items in datadir" % i)




                            
                


        
        
