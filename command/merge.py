# -*- coding: utf-8 -*-

import sys

from yacite.types import Datadir
from yacite.exception import *
from yacite.types import BibObject
from yacite.utils.sane_yaml import docstream
from yacite.utils.misc import describe_item


class Merge(object):


    help="merge records with datadir - see the docs for merge rules"

    @staticmethod
    def add_arguments(subparser):
        subparser.add_argument("datadir")
        subparser.add_argument("-u","--union",help="take union of lists - original and new",
            dest="uname",action="append",default=[])
        subparser.add_argument("-s","--set",help="replace orginal values by new value",
            dest="sname",action="append",default=[])
        subparser.add_argument("-d","--delete-field",help="delete field",dest="dname",action="append",
            default=[])
        subparser.add_argument("-v","--verbose",action="store_true",help="be verbose")
        subparser.add_argument("-q","--quiet",action="store_true",help="be quiet")

    def __init__(self,ns):
        self.verbose=ns.verbose
        self.quiet=ns.quiet
        self.datadir_name=ns.datadir
        self.datadir=Datadir(self.datadir_name)
        self.union_names=ns.uname
        self.set_names=ns.sname
        self.delete_names=ns.dname

    def execute(self):

        bounces=0
        for i,d in enumerate(docstream(sys.stdin)):
            if type(d) is not dict:
                raise DataError("merge: expecting dict as item %s in stream, got %s instead" % (describe_item(i,d),type(d)))
            matches=self.datadir.list_matching(d)
            if len(matches)>1:
                raise DataError("merge: %s in stream matches multiple items in datadir" %  describe_item(i,d))
            elif len(matches)==1:
                match=matches[0]
                bounced=True
                for key in d:
                    if (key in self.set_names) or (key not in match):
                        match[key]=d[key]
                        bounced=False
                        continue
                    elif (key in self.union_names) and (key in match):
                        if type(d[key]) is list and type(match[key]) is list:
                            match[key].extend(d[key])
                            match[key]=list(set(match[key]))
                            bounced=False
                            continue
                        else:
                            raise DataError(
                             "merge: union of non-lists requested: %s in stream, file='%s', name='%s"
                                % (describe_item(i,d),match.path,key))
                    elif key in self.delete_names and key in match:
                        del match[key]
                        bounced=False
                        match.dirty=True
                if bounced:
                    bounces=bounces+1
                    if self.verbose:
                        print >>sys.stderr,"%s matches uniquely file '%s', but no change requested" % (describe_item(i,d),match.path)
                match.save()
            else:
                newitem=BibObject(d,datadir=self.datadir)
                newitem.dirty=True
                newitem.save()
                self.datadir.append(newitem)
        if bounces and not self.quiet:
            print >>sys.stderr,"merge: %d items matched uniquely, but no change in them was requested." % bounces
            print >>sys.stderr,"merge: Use -v to see identify these items, use -q to supress this message." 
        
