# -*- coding: utf-8 -*-

import sys

from yacite.types import Datadir
from yacite.exception import *
from yacite.types import BibRecord
from yacite.utils.sane_yaml import record_stream
from yacite.utils.misc import describe_record


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
        for i,rec in enumerate(record_stream(sys.stdin)):
            if type(rec) is not dict:
                raise DataError("merge: expecting dict as %s in stream, got %s instead" % (describe_record(i,rec),type(rec)))
            matches=self.datadir.list_matching(rec)
            if len(matches)>1:
                raise DataError("merge: %s in stream matches multiple records in datadir" %  describe_record(i,rec))
            elif len(matches)==1:
                match=matches[0]
                bounced=True
                for field_name in rec:
                    if (field_name in self.set_names) or (field_name not in match):
                        if not self.quiet:
                            print >>sys.stderr,"merge: SET %s[%s] to %s" %(match["key"],field_name,rec[field_name])
                        match[field_name]=rec[field_name]
                        bounced=False
                        continue
                    elif (field_name in self.union_names) and (field_name in match):
                        if type(rec[field_name]) is list and type(match[field_name]) is list:
                            match[field_name].extend(rec[field_name])
                            match[field_name]=list(set(match[field_name]))
                            if not self.quiet:
                                print >>sys.stderr,"merge: SET %s[%s] to %s (union)" %(match["key"],field_name,match[field_name])
                            bounced=False
                            continue
                        else:
                            raise DataError(
                             "merge: union of non-lists requested: %s in stream, file='%s', name='%s"
                                % (describe_record(i,rec),match.path,field_name))
                    elif field_name in self.delete_names and field_name in match:
                        del match[field_name]
                        if not self.quiet:
                            print >>sys.stderr,"merge: DELETE %s[%s]" %(match["key"],field_name)
                        bounced=False
                        match.dirty=True
                if bounced:
                    diff=[field_name for field_name in set(rec)&set(match) 
                        if rec[field_name]!=match[field_name]]
                    if diff:
                        bounces=bounces+1
                    if self.verbose and diff:
                        print >>sys.stderr,"merge: %s matches uniquely file '%s', differs from it, but no change was requested; field(s) %s differ" % (describe_record(i,rec),match.path,",".join(diff))
                match.save()
            else:
                newrecord=BibRecord(rec,datadir=self.datadir)
                newrecord.dirty=True
                newrecord.save()
                self.datadir.append(newrecord)
        if bounces and not self.quiet:
            print >>sys.stderr,"merge: %d records matched uniquely, but no change in them was requested." % bounces
            print >>sys.stderr,"merge: Use -v to see identify these records, use -q to supress this message."      
